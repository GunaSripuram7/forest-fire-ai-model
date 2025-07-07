import rasterio
import numpy as np
from rasterio.enums import Resampling
from scipy.ndimage import sobel

def compute_slope(dem: np.ndarray, resolution: float) -> np.ndarray:
    # Compute gradients
    dzdx = sobel(dem, axis=1) / (8.0 * resolution)
    dzdy = sobel(dem, axis=0) / (8.0 * resolution)
    slope = np.sqrt(dzdx**2 + dzdy**2)
    # Normalize slope to [0,1]
    slope_norm = (slope - slope.min()) / (slope.max() - slope.min() + 1e-6)
    return slope_norm

if __name__ == "__main__":
    in_path = "data/processed/terrain/dem_clipped.tif"
    out_path = "data/processed/terrain/dem_slope_11x13.tif"

    with rasterio.open(in_path) as src:
        dem = src.read(1).astype(np.float32)
        profile = src.profile
        resolution = src.res[0]  # Assuming square pixels

    slope_norm = compute_slope(dem, resolution)

    profile.update(dtype=rasterio.float32, count=1)
    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(slope_norm.astype(np.float32), 1)

    print(f"Slope written to {out_path}")
