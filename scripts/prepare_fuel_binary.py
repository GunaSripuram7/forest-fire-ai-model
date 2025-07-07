import rasterio
import numpy as np

def create_binary_fuel(lc: np.ndarray) -> np.ndarray:
    # Classes 1-10 are flammable: forest, shrub, grassland, cropland
    return np.where((lc >= 1) & (lc <= 10), 1, 0).astype(np.uint8)

if __name__ == "__main__":
    in_path = "data/processed/fuel/fuel_clipped.tif"
    out_path = "data/processed/fuel/fuel_binary_11x13.tif"

    with rasterio.open(in_path) as src:
        lc_type = src.read(1)
        profile = src.profile

    binary_fuel = create_binary_fuel(lc_type)
    profile.update(dtype=rasterio.uint8, count=1)

    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(binary_fuel, 1)

    print(f"Binary fuel saved to {out_path}")
