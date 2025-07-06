import pandas as pd

# Load fire data
df = pd.read_csv("data/raw/fire_history/MODIS_C6_1_Global_24h.csv")

# Show structure
print("🔥 Columns:", df.columns.tolist())

# Show coordinate range
print("🌎 Latitude range:", df['latitude'].min(), "to", df['latitude'].max())
print("🌍 Longitude range:", df['longitude'].min(), "to", df['longitude'].max())

# Preview some entries
print("\n📌 Sample fire points:")
print(df[['latitude', 'longitude', 'acq_date']].head(10))
