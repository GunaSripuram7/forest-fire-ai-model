# scripts/download_ghsl_builtin.py
import os
import requests
import rasterio
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import box

# Define bbox
minx, miny, maxx, maxy = 130.5, -13.5, 133.5, -11.0

# GHSL site provides tile structure; replace '<tile_url>' with real URL
# Example tile name: 'GHS_BUILT_LDSMT_GLOBE_R2018A_3857_30S11E130.tif'
tiles = [
    "S11E130", "S11E131", "S11E132", "S11E133",
    "S12E130", "S12E131", "S12E132", "S12E133"
]


output_dir = "data/raw/human/ghsl"
os.makedirs(output_dir, exist_ok=True)

for t in tiles:
    url = f"https://ghsl.jrc.ec.europa.eu/do_download/GHS_BUILT_LDSMT_GLOBE_R2018A_3857_30{t}.zip"
    local_zip = os.path.join(output_dir, f"{t}.zip")
    if not os.path.exists(local_zip):
        print(f"⬇️ Downloading {t}...")
        r = requests.get(url)
        if r.ok:
            with open(local_zip, "wb") as f:
                f.write(r.content)

print("✅ GHSL downloaded (tiles). Remember to unzip and clip to your bbox.")
