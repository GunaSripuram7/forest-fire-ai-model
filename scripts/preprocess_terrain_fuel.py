import os
import glob
import rasterio
from rasterio.merge import merge
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
from shapely.geometry import box
import geopandas as gpd
from osgeo import gdal

# Common parameters
bbox = [130.5, -13.5, 133.5, -11.0]  # [minx, miny, maxx, maxy]
pixel_size = 0.0003  # ~30m in degrees
crs_wgs84 = 'EPSG:4326'

# Directories
raw_terrain_dir  = 'data/raw/terrain'
raw_fuel_dir     = 'data/raw/fuel'
proc_terrain_dir = 'data/processed/terrain'
proc_fuel_dir    = 'data/processed/fuel'

os.makedirs(proc_terrain_dir, exist_ok=True)
os.makedirs(proc_fuel_dir, exist_ok=True)

# -----------------------
# 1) PREPROCESS TERRAIN
# -----------------------
terrain_files = glob.glob(os.path.join(raw_terrain_dir, '*.tif'))
srcs = [rasterio.open(fp) for fp in terrain_files]
mosaic, out_trans = merge(srcs)
meta = srcs[0].meta.copy()
meta.update({
    'height': mosaic.shape[1],
    'width': mosaic.shape[2],
    'transform': out_trans,
    'crs': srcs[0].crs
})
merged_dem = os.path.join(proc_terrain_dir, 'dem_merged.tif')
with rasterio.open(merged_dem, 'w', **meta) as dst:
    dst.write(mosaic)
print(f'✅ Merged DEM: {merged_dem}')

# Clip DEM to bounding box
geom = [box(*bbox)]
gdf = gpd.GeoDataFrame({'geometry': geom}, crs=crs_wgs84)
with rasterio.open(merged_dem) as src:
    clipped_dem, transform = mask(src, gdf.geometry, crop=True)
clip_meta = src.meta.copy()
clip_meta.update({
    'height': clipped_dem.shape[1],
    'width': clipped_dem.shape[2],
    'transform': transform
})
clipped_dem_path = os.path.join(proc_terrain_dir, 'dem_clipped.tif')
with rasterio.open(clipped_dem_path, 'w', **clip_meta) as dst:
    dst.write(clipped_dem)
print(f'✅ Clipped DEM: {clipped_dem_path}')

# -----------------------
# 2) PREPROCESS FUEL (MCD12Q1 HDF)
# -----------------------
hdf_files = glob.glob(os.path.join(raw_fuel_dir, '*.hdf'))
fuel_tifs = []

for hdf_path in hdf_files:
    print(f"📂 Processing HDF: {hdf_path}")
    hdf_dataset = gdal.Open(hdf_path)
    subdatasets = hdf_dataset.GetSubDatasets()

    # Search for LC_Type1 subdataset
    lc_type1_subds = None
    for name, desc in subdatasets:
        if 'LC_Type1' in name:
            lc_type1_subds = name
            break

    if lc_type1_subds is None:
        print(f"❌ LC_Type1 not found in {hdf_path}")
        continue

    # Step 1: Extract LC_Type1 to temp file (original projection)
    temp_path = os.path.join(
        proc_fuel_dir,
        os.path.basename(hdf_path).replace('.hdf', '_temp.tif')
    )
    gdal.Translate(temp_path, lc_type1_subds)

    # Step 2: Reproject to EPSG:4326
    out_path = os.path.join(
        proc_fuel_dir,
        os.path.basename(hdf_path).replace('.hdf', '_LC_Type1.tif')
    )
    gdal.Warp(out_path, temp_path, dstSRS='EPSG:4326')
    os.remove(temp_path)  # Clean up temporary file

    fuel_tifs.append(out_path)
    print(f"✅ Extracted & Reprojected LC_Type1 to: {out_path}")

# ✅ Step 3: Merge all reprojected fuel .tif files
srcs_fuel = [rasterio.open(fp) for fp in fuel_tifs]
m_fuel, t_fuel = merge(srcs_fuel)
fuel_meta = srcs_fuel[0].meta.copy()
fuel_meta.update({
    'height': m_fuel.shape[1],
    'width': m_fuel.shape[2],
    'transform': t_fuel
})
merged_fuel = os.path.join(proc_fuel_dir, 'fuel_merged.tif')
with rasterio.open(merged_fuel, 'w', **fuel_meta) as dst:
    dst.write(m_fuel)
print(f'✅ Merged Fuel: {merged_fuel}')

# ✅ Step 4: Clip merged fuel to bounding box
with rasterio.open(merged_fuel) as src:
    clipped_fuel, transform_f = mask(src, gdf.geometry, crop=True)
clip_fuel_meta = src.meta.copy()
clip_fuel_meta.update({
    'height': clipped_fuel.shape[1],
    'width': clipped_fuel.shape[2],
    'transform': transform_f
})
clipped_fuel_path = os.path.join(proc_fuel_dir, 'fuel_clipped.tif')
with rasterio.open(clipped_fuel_path, 'w', **clip_fuel_meta) as dst:
    dst.write(clipped_fuel)
print(f'✅ Clipped Fuel: {clipped_fuel_path}')
