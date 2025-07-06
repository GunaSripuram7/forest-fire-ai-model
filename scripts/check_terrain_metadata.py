import os
import glob
import rasterio

terrain_folder = "data/raw/terrain/"
tif_files = sorted(glob.glob(os.path.join(terrain_folder, "*.tif")))

crs_set = set()
res_set = set()

for tif in tif_files:
    with rasterio.open(tif) as src:
        print(f"{os.path.basename(tif)}: CRS={src.crs}, Resolution={src.res}, Bounds={src.bounds}")
        crs_set.add(src.crs)
        res_set.add(src.res)

print("\n✅ Unique CRS found:", crs_set)
print("✅ Unique Resolutions found:", res_set)
