import dask.dataframe as dd
from dask.diagnostics import ProgressBar
import os

raw_data_path = os.path.expanduser("C:/Users/durki/OneDrive/Desktop/MIS581/data/region_10000002_orders.parquet")
output_parquet_path = os.path.expanduser("C:/Users/durki/OneDrive/Desktop/MIS581/data/region_10000002_orders/partitioned_market_orders")

# Defining data types to prevent Dask memory mapping errors
dtypes = {
    'transaction_id': 'string',
    'is_buy_order': 'boolean',
    'type_id': 'Int64',
    'system_id': 'Int64',
    'price_isk': 'float64',
    'volume_total': 'Int64',
    'event_category': 'string',
    'destroyed_isk': 'float64'
}

# Ingest raw CSV data
ddf = dd.read_parquet(raw_data_path)

# Cleane missing partition keys to prevent pyarrow errors
ddf = ddf.dropna(subset=['system_id'])

# Execute parallel write
print("Initiating Dask parallel pricessing. Converting to partitioned Parquet...")
with ProgressBar():
    ddf.to_parquet(
        output_parquet_path,
        engine='pyarrow',
        partition_on=['system_id'],
        write_index=False
    )
print("Conversion complete: Data is now partitioned.")