import os
import requests

# ✅ Guaranteed working fire data (MODIS Global - April 1, 2024)
firms_url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis/c6.1/global/2024/MODIS_C6_1_Global_20240401.txt"

# Save to raw fire_history folder
output_dir = "data/raw/fire_history"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "modis_fires_global_20240401.csv")

# Download
response = requests.get(firms_url)

if response.status_code == 200:
    with open(output_file, "wb") as f:
        f.write(response.content)
    print(f"✅ Fire data saved to: {output_file}")
else:
    print(f"❌ Failed to download. Status: {response.status_code}")
