# scripts/rasterize_fire_labels.py

import os
import pandas as pd
import rasterio
from rasterio.transform import from_origin
from rasterio.features import rasterize
from shapely.geometry import Point
import numpy as np

# ✅ Load fire CSV from raw folder
fire_csv_path = os.path.join("data", "raw", "fire_history", "fire_20210419_24h_modis.csv")
fire_df = pd.read_csv(fire_csv_path)  # ✅ Use the header row


# ✅ Extract lat/lon points
points = [Point(lon, lat) for lat, lon in zip(fire_df["latitude"], fire_df["longitude"])]

# ✅ Define raster grid parameters (same as weather TIF region)
pixel_size = 0.0003  # ~30m resolution at equator
min_lon, max_lon = 130.5, 133.5
min_lat, max_lat = -13.5, -11

width = int((max_lon - min_lon) / pixel_size)
height = int((max_lat - min_lat) / pixel_size)
transform = from_origin(min_lon, max_lat, pixel_size, pixel_size)

# ✅ Rasterize fire points as binary mask
fire_mask = rasterize(
    [(p, 1) for p in points],
    out_shape=(height, width),
    transform=transform,
    fill=0,
    dtype=np.uint8
)

# ✅ Save to processed folder
# Ensure subfolder exists
os.makedirs("data/processed/fire", exist_ok=True)

# Save raster here
out_path = "data/processed/fire_labels/fire_20210419_label.tif"
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with rasterio.open(
    out_path,
    "w",
    driver="GTiff",
    height=height,
    width=width,
    count=1,
    dtype=fire_mask.dtype,
    crs="EPSG:4326",
    transform=transform
) as dst:
    dst.write(fire_mask, 1)

print(f"✅ Fire label raster saved at: {out_path}")
