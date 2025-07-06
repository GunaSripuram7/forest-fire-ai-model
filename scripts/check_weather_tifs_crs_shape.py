import rasterio

crs_set = set()
shape_set = set()

for var in ['t2m', 'u10', 'v10', 'precip']:
    for i in range(24):
        path = f"data/processed/weather_tifs/{var}_{i:02d}.tif"
        with rasterio.open(path) as src:
            crs_set.add(str(src.crs))
            shape_set.add(src.shape)

print("✅ CRS used:", crs_set)
print("✅ Unique shapes found:", shape_set)
