# scripts/debug_check_fuel_bbox.py

import rasterio

fuel_path = "data/processed/fuel/fuel_merged.tif"
with rasterio.open(fuel_path) as src:
    bounds = src.bounds
    print("🗺️  Fuel Raster Bounds:")
    print(f"  Left:   {bounds.left}")
    print(f"  Bottom: {bounds.bottom}")
    print(f"  Right:  {bounds.right}")
    print(f"  Top:    {bounds.top}")
