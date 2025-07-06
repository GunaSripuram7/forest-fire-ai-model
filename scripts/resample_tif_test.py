import rasterio
from rasterio.enums import Resampling

src_path = "data/processed/weather_tifs/t2m_00.tif"
dst_path = "data/processed/weather_tifs/t2m_00_resampled.tif"

with rasterio.open(src_path) as src:
    upscale_factor = 2
    new_height = int(src.height * upscale_factor)
    new_width = int(src.width * upscale_factor)
    data = src.read(
        out_shape=(1, new_height, new_width),
        resampling=Resampling.bilinear
    )
    transform = src.transform * src.transform.scale(
        src.width / new_width,
        src.height / new_height
    )
    with rasterio.open(
        dst_path,
        "w",
        driver="GTiff",
        height=new_height,
        width=new_width,
        count=1,
        dtype=data.dtype,
        crs=src.crs,
        transform=transform,
    ) as dst:
        dst.write(data)
