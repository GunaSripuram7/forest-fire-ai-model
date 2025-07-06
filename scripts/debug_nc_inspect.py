import xarray as xr

ds = xr.open_dataset("data/raw/weather/data_stream-oper_stepType-instant.nc")
print(ds)
