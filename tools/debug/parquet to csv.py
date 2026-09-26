import pandas as pd

# Load the Parquet file into a DataFrame
df = pd.read_parquet('C:/Users/durki/OneDrive/Desktop/MIS581/data/region_10000030_orders/partitioned_market_orders/system_id=30002505/part.0.parquet')

# Convert and save as a standard JSON array of records
df.to_csv('market_orders_1.csv', index=False)