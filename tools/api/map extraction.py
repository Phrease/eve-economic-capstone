import pandas as pd
import os

# Fetch latest static solar system
print("Downloading static geography tables...")
df_systems = pd.read_csv("https://www.fuzzwork.co.uk/dump/latest/csv/mapSolarSystems.csv")
df_regions = pd.read_csv("https://www.fuzzwork.co.uk/dump/latest/csv/mapRegions.csv")

# Merge the df's on regionID for mapping
df_merged = pd.merge(df_systems, df_regions, on='regionID', how='left')

# Filter and rename columns to match dim_geography
dim_geo = df_merged[['solarSystemID', 'regionID', 'solarSystemName', 'regionName']].copy()
dim_geo.columns = ['system_id', 'region_id', 'system_name', 'region_name']

# Flagging Jita as the singular central trade hub
dim_geo['is_central_hub'] = dim_geo['system_id'] == 30000142

# Save to local directory
csv_path = os.path.expanduser("C:/Users/durki/OneDrive/Desktop/MIS581/data/dim_geography.csv")
dim_geo.to_csv(csv_path, index=False)
print(f"Geographic mapping saved to {csv_path}")