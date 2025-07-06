# scripts/download_fuel_lpdaac.py

import os
from earthaccess import Auth, DataCollections, DataGranules

# ✅ Authenticate with NASA Earthdata
auth = Auth()
auth.login(strategy="netrc")  # Will read ~/.netrc

# ✅ Define MODIS Land Cover Collection (v6.1)
COLLECTION_ID = "C2070783083-LPCLOUD"  # MCD12Q1.061

# ✅ Define correct region and time
start_date = "2021-01-01"
end_date = "2021-12-31"

# ✅ MODIS tile IDs for NT-Australia region (adjusted)
tiles = ["h30v10", "h31v10"]


# ✅ Output directory
output_dir = "data/raw/fuel"
os.makedirs(output_dir, exist_ok=True)

# ✅ Download per tile
for tile in tiles:
    print(f"🔍 Searching for: {tile}")
    results = DataGranules().cloud_hosted().short_name("MCD12Q1")\
        .version("061").temporal(start_date, end_date)\
        .bounding_box(129.5, -14.5, 134.5, -11)\
        .granule_name(f"*{tile}*")\
        .get_all()

    print(f"✅ Found {len(results)} granules for {tile}")

    for granule in results:
        print(f"⬇️  Downloading {granule.umm['GranuleUR']} ...")
        granule.download(output_dir)
