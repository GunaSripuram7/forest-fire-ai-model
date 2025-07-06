import os
import glob
import rasterio
from rasterio.merge import merge
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd

# ✅ Paths
input_dir = "data/raw/human/ghsl"
output_dir = "data/processed/human"
os.makedirs(output_dir, exist_ok=True)

merged_path = os.path.join(output_dir, "ghsl_merged_moll.tif")
reprojected_path = os.path.join(output_dir, "ghsl_wgs84.tif")
final_clipped_path = os.path.join(output_dir, "ghsl_builtup_clipped.tif")

# ✅ Step 1: Merge
src_files = glob.glob(os.path.join(input_dir, "*.tif"))
src_list = [rasterio.open(f) for f in src_files]
mosaic, out_trans = merge(src_list)
meta = src_list[0].meta.copy()
meta.update({
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_trans
})
with rasterio.open(merged_path, "w", **meta) as dst:
    dst.write(mosaic)
print(f"✅ Merged: {merged_path}")

# ✅ Step 2: Reproject to EPSG:4326
dst_crs = "EPSG:4326"
transform, width, height = calculate_default_transform(
    meta["crs"], dst_crs,
    meta["width"], meta["height"], *src_list[0].bounds
)
reprojected_meta = meta.copy()
reprojected_meta.update({
    "crs": dst_crs,
    "transform": transform,
    "width": width,
    "height": height
})

with rasterio.open(reprojected_path, "w", **reprojected_meta) as dst:
    for i in range(1, mosaic.shape[0] + 1):
        reproject(
            source=mosaic[i - 1],
            destination=rasterio.band(dst, i),
            src_transform=out_trans,
            src_crs=meta["crs"],
            dst_transform=transform,
            dst_crs=dst_crs,
            resampling=Resampling.nearest
        )
print(f"✅ Reprojected: {reprojected_path}")

# ✅ Step 3: Clip to NT-Australia region
bbox = box(130.5, -13.5, 133.5, -11.0)
gdf = gpd.GeoDataFrame({"geometry": [bbox]}, crs=dst_crs)

with rasterio.open(reprojected_path) as src:
    out_image, out_transform = mask(src, gdf.geometry, crop=True)
    clipped_meta = src.meta.copy()
    clipped_meta.update({
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

with rasterio.open(final_clipped_path, "w", **clipped_meta) as dst:
    dst.write(out_image)
print(f"✅ Final Clipped Built-up Saved: {final_clipped_path}")
