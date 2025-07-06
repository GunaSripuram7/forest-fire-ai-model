# scripts/inspect_hdf_subdatasets.py

import os
from osgeo import gdal

# Directory containing your HDF fuel files
raw_fuel_dir = 'data/raw/fuel'

# Find all .hdf files in folder
hdf_files = [os.path.join(raw_fuel_dir, f)
             for f in os.listdir(raw_fuel_dir)
             if f.lower().endswith('.hdf')]

if not hdf_files:
    print('❌ No HDF files found in:', raw_fuel_dir)
    exit(1)

# Inspect each HDF for subdatasets
for hdf_path in hdf_files:
    print(f"\nInspecting: {hdf_path}")
    ds = gdal.Open(hdf_path)
    if ds is None:
        print("  ❌ Failed to open HDF file")
        continue

    subdatasets = ds.GetSubDatasets()
    if not subdatasets:
        print("  ⚠️ No subdatasets found.")
    else:
        print(f"  Found {len(subdatasets)} subdatasets:")
        for idx, (name, desc) in enumerate(subdatasets):
            print(f"    [{idx}] {name}\n        -> {desc}")

print("\n✅ Inspection complete.")
