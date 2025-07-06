import os
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.windows import Window

# Input: high-res fire label (rasterized already)
fire_label_path = "data/processed/fire_labels/fire_20210419_label.tif"
downsampled_path = "data/processed/fire_labels/fire_20210419_downsampled_11x13.tif"

# Target resolution from weather data
target_height, target_width = 11, 13

with rasterio.open(fire_label_path) as src:
    # Read the full raster
    fire_data = src.read(1)
    original_height, original_width = fire_data.shape

    # Compute size of each coarse block
    block_height = original_height // target_height
    block_width = original_width // target_width

    # Create downsampled array (binary mask)
    downsampled = np.zeros((target_height, target_width), dtype=np.uint8)

    for i in range(target_height):
        for j in range(target_width):
            y_start = i * block_height
            x_start = j * block_width
            window = fire_data[y_start:y_start + block_height, x_start:x_start + block_width]

            # If any pixel in this block is fire (non-zero), mark as 1
            downsampled[i, j] = 1 if np.any(window > 0) else 0

    # Save the downsampled fire mask
    transform = src.transform * src.transform.scale(
        src.width / target_width,
        src.height / target_height
    )

    os.makedirs(os.path.dirname(downsampled_path), exist_ok=True)

    with rasterio.open(
        downsampled_path,
        "w",
        driver="GTiff",
        height=target_height,
        width=target_width,
        count=1,
        dtype=np.uint8,
        crs=src.crs,
        transform=transform,
    ) as dst:
        dst.write(downsampled, 1)

print(f"✅ Downsampled fire label saved at: {downsampled_path}")
