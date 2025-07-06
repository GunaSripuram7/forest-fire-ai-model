import os
import glob
import rasterio
import matplotlib.pyplot as plt

# Folder containing your .tif files
terrain_folder = "data/raw/terrain/"
tif_files = sorted(glob.glob(os.path.join(terrain_folder, "*.tif")))

# Plot all tiles (quick check)
fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(16, 12))
axes = axes.flatten()

for i, tif in enumerate(tif_files):
    with rasterio.open(tif) as src:
        img = src.read(1)
        axes[i].imshow(img, cmap='terrain')
        axes[i].set_title(os.path.basename(tif))
        axes[i].axis('off')

# Hide unused axes (if less than 16)
for j in range(i+1, len(axes)):
    axes[j].axis('off')

plt.tight_layout()
plt.show()
