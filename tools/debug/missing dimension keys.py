import pandas as pd
import dask.dataframe as dd
from pathlib import Path
import glob

data_dir = Path("C:/Users/durki/OneDrive/Desktop/MIS581/data")

# Load existing dimension keys
dim_item = pd.read_csv(data_dir / "dim_item.csv")
dim_geo = pd.read_csv(data_dir / "dim_geography.csv")

existing_type_ids = set(dim_item['type_id'])
existing_system_ids = set(dim_geo['system_id'])

# Gather all new regional parquet files (excluding the partitioned folders)
parquet_files = glob.glob(str(data_dir / "region_*_orders.parquet"))

new_type_ids = set()
new_system_ids = set()

# Extract unique IDs from all new regions
for file in parquet_files:
    df = dd.read_parquet(file)
    
    # Compute unique IDs for this specific region
    unique_types = set(df['type_id'].unique().compute())
    unique_systems = set(df['system_id'].unique().compute())
    
    new_type_ids.update(unique_types)
    new_system_ids.update(unique_systems)

# Filter for only the IDs missing from your database
missing_types = list(new_type_ids - existing_type_ids)
missing_systems = list(new_system_ids - existing_system_ids)

print(f"Missing Item Types to Fetch: {len(missing_types)}")
print(missing_types)
print(f"Missing Solar Systems to Fetch: {len(missing_systems)}")
print(missing_systems)