import rasterio
import numpy as np

for var in ['t2m', 'u10', 'v10', 'precip']:
    for i in range(24):
        path = f"data/processed/weather_tifs/{var}_{i:02d}.tif"
        with rasterio.open(path) as src:
            data = src.read(1)
            if np.isnan(data).all():
                print(f"❌ {var}_{i:02d}.tif: All values are NaN")
            elif np.max(data) == 0:
                print(f"⚠️ {var}_{i:02d}.tif: All values are 0")
            else:
                print(f"✅ {var}_{i:02d}.tif is OK")
