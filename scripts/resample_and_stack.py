# scripts/resample_and_stack.py

import os
import glob
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling

# Paths
weather_dir = "data/processed/weather_tifs"
dem_path    = "data/processed/terrain/dem_clipped.tif"
fuel_path   = "data/processed/fuel/fuel_clipped.tif"
human_path  = "data/processed/human/ghsl_builtup_clipped.tif"
stack_out   = "data/processed/feature_stack.npz"

# 1) Load weather grid reference
weather_files = sorted(glob.glob(os.path.join(weather_dir, "*.tif")))
with rasterio.open(weather_files[0]) as ref:
    H, W      = ref.height, ref.width
    transform = ref.transform
    crs       = ref.crs
    profile   = ref.profile

# Read all weather bands into (H, W, T)
weather_stack = np.zeros((H, W, len(weather_files)), dtype=np.float32)
for i, fp in enumerate(weather_files):
    with rasterio.open(fp) as src:
        weather_stack[:, :, i] = src.read(1)

# 2) Resample single-band raster to weather grid
def load_and_resample(path):
    with rasterio.open(path) as src:
        data = src.read(1)
        dst = np.zeros((H, W), dtype=data.dtype)
        reproject(
            source=data,
            destination=dst,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=transform,
            dst_crs=crs,
            resampling=Resampling.bilinear
        )
    return dst

# 3) Resample terrain, fuel, human
dem   = load_and_resample(dem_path)
fuel  = load_and_resample(fuel_path)
human = load_and_resample(human_path)

# 4) Stack into (H, W, F)
feature_stack = np.dstack([weather_stack, dem[:, :, None], fuel[:, :, None], human[:, :, None]])
print(f"Feature stack shape: {feature_stack.shape}")  # Expect (11, 13, F)

# 5) Save stack
np.savez_compressed(stack_out, features=feature_stack)
print("✅ Saved feature stack to", stack_out)
