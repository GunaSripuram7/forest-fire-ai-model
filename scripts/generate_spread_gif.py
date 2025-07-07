import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# === Define hours to animate ===
timesteps = [1, 2, 3, 6, 12]

# === Load and plot spread data into PNGs ===
png_paths = []
for hour in timesteps:
    fig, ax = plt.subplots(figsize=(5, 5))
    arr = plt.imread(f"outputs/fire_spread_t_plus_{hour}h.tif")
    ax.imshow(arr, cmap='hot', vmin=0, vmax=1)
    ax.set_title(f"Fire Spread at t+{hour}h")
    ax.axis('off')

    png_path = f"outputs/frame_t_plus_{hour}h.png"
    plt.savefig(png_path, bbox_inches='tight')
    plt.close(fig)
    png_paths.append(png_path)

# === Load PNGs as PIL images ===
frames = [Image.open(path).convert("RGB") for path in png_paths]

# === Save as animated GIF ===
gif_path = "outputs/fire_spread_animation.gif"
frames[0].save(
    gif_path,
    save_all=True,
    append_images=frames[1:],
    duration=2500,  # 2.5 seconds per frame
    loop=0  # play only once
)

print(f"🎞️ Fire spread animation saved to {gif_path}")

# === Optional: remove temporary PNGs ===
for path in png_paths:
    os.remove(path)
