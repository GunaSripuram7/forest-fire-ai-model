import xarray as xr
import rasterio
from rasterio.transform import from_origin
import numpy as np
import os

# Paths to your extracted files
instant_nc = "data/raw/weather/data_stream-oper_stepType-instant.nc"
accum_nc = "data/raw/weather/data_stream-oper_stepType-accum.nc"


# Output folder
os.makedirs("data/processed/weather_tifs/", exist_ok=True)

# Helper to export each hour of a variable as a tif
def save_variable_as_tif(ds, var_name, output_prefix):
    time_coord = 'time' if 'time' in ds.coords else 'valid_time'
    for i, t in enumerate(ds[time_coord]):
        data = ds[var_name].isel({time_coord: i}).squeeze().values
        lat = ds.latitude.values
        lon = ds.longitude.values
        transform = from_origin(lon.min(), lat.max(), abs(lon[1]-lon[0]), abs(lat[1]-lat[0]))
        
        # Flip lat axis if needed
        if lat[0] < lat[-1]:
            data = np.flipud(data)
        
        with rasterio.open(
            f"data/processed/weather_tifs/{output_prefix}_{i:02d}.tif", "w",
            driver="GTiff",
            height=data.shape[0],
            width=data.shape[1],
            count=1,
            dtype=data.dtype,
            crs="EPSG:4326",
            transform=transform
        ) as dst:
            dst.write(data, 1)

# Open .nc files and extract variables
ds_instant = xr.open_dataset(instant_nc)
ds_accum = xr.open_dataset(accum_nc)

# Save temperature, wind u/v
save_variable_as_tif(ds_instant, "u10", "u10")         # 10m u-wind
save_variable_as_tif(ds_instant, "v10", "v10")         # 10m v-wind
save_variable_as_tif(ds_instant, "t2m", "t2m")         # 2m temperature

# Save precipitation
save_variable_as_tif(ds_accum, "tp", "precip")         # total precipitation
