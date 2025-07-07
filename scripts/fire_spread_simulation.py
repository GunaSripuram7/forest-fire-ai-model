import numpy as np
import rasterio
from rasterio import Affine
import matplotlib.pyplot as plt
import os

def spread_one_hour(current_mask: np.ndarray,
                    wind_u: np.ndarray,
                    wind_v: np.ndarray,
                    slope: np.ndarray,
                    fuel: np.ndarray,
                    ignition_prob: float = 0.3) -> np.ndarray:
    """
    Simulate one hour of fire spread using a simple CA rule:
      - For each currently burning cell, attempt to ignite its 8 neighbors
      - Ignition probability increases with wind alignment, fuel presence, and slope
    """
    rows, cols = current_mask.shape
    next_ignitions = np.zeros_like(current_mask)

    # Define 8-neighbor offsets
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),           (0, 1),
                 (1, -1),  (1, 0),  (1, 1)]

    for i in range(rows):
        for j in range(cols):
            if current_mask[i, j] == 1:
                for di, dj in neighbors:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if current_mask[ni, nj] == 0 and fuel[ni, nj] == 1:
                            wind_alignment = wind_u[i, j] * di + wind_v[i, j] * dj
                            wind_factor = max(0, wind_alignment) / (np.hypot(wind_u[i, j], wind_v[i, j]) + 1e-6)
                            prob = ignition_prob * (1 + wind_factor) * (1 + slope[ni, nj])
                            if np.random.rand() < prob:
                                next_ignitions[ni, nj] = 1
    return next_ignitions


if __name__ == "__main__":
    # === File paths ===
    mask_path = 'data/processed/fire_labels/fire_20210419_downsampled_11x13.tif'
    timesteps = [1, 2, 3, 6, 12]
    wind_u_paths = [f"data/processed/weather_tifs/u10_{h:02d}.tif" for h in timesteps]
    wind_v_paths = [f"data/processed/weather_tifs/v10_{h:02d}.tif" for h in timesteps]
    slope_path = 'data/processed/terrain/dem_slope_11x13.tif'
    fuel_path = 'data/processed/fuel/fuel_binary_11x13.tif'

    # === Load input layers ===
    with rasterio.open(mask_path) as src:
        profile = src.profile
        pred_mask = src.read(1).astype(np.uint8)
    with rasterio.open(slope_path) as src:
        slope = src.read(1).astype(np.float32)
    with rasterio.open(fuel_path) as src:
        fuel = src.read(1).astype(np.uint8)

    # === Initialize spread ===
    cum_mask = pred_mask.copy()
    results = {}

    for idx, (u_path, v_path) in enumerate(zip(wind_u_paths, wind_v_paths)):
        hour = timesteps[idx]

        with rasterio.open(u_path) as src_u, rasterio.open(v_path) as src_v:
            wind_u = src_u.read(1)
            wind_v = src_v.read(1)

        new_ignitions = spread_one_hour(cum_mask, wind_u, wind_v, slope, fuel)
        cum_mask = np.clip(cum_mask + new_ignitions, 0, 1)
        results[hour] = cum_mask.copy()

        # === Save raster ===
        out_path = f'outputs/fire_spread_t_plus_{hour}h.tif'
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        profile.update(dtype=rasterio.uint8, count=1)
        with rasterio.open(out_path, 'w', **profile) as dst:
            dst.write(cum_mask.astype(np.uint8), 1)
        print(f"✅ Saved t+{hour}h spread raster to {out_path}")

    # === Plot all timesteps in one figure ===
    fig, axs = plt.subplots(1, len(timesteps), figsize=(4 * len(timesteps), 4))
    for i, hour in enumerate(timesteps):
        axs[i].imshow(results[hour], cmap='hot', vmin=0, vmax=1)
        axs[i].set_title(f't+{hour}h')
        axs[i].axis('off')
    plt.tight_layout()

    # Save the visual plot
    plot_path = "outputs/spread_comparison.png"
    plt.savefig(plot_path)
    print(f"📊 Spread comparison plot saved to {plot_path}")
