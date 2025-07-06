import rasterio
import matplotlib.pyplot as plt

file = "data/processed/weather_tifs/t2m_14.tif"

with rasterio.open(file) as src:
    data = src.read(1)

plt.imshow(data, cmap="inferno")
plt.colorbar()
plt.title("T2M at Hour 14")
plt.show()
