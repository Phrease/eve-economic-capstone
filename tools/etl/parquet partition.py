import dask.dataframe as dd
from dask.diagnostics import ProgressBar
from pathlib import Path
import os

base_dir = Path(os.path.expanduser("C:/Users/durki/OneDrive/Desktop/MIS581/data"))

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

def process_regional_partitions():
    # Final all region parquet files in the data directory
    parquet_files = list(base_dir.glob("region_*_orders.parquet"))

    if not parquet_files:
        print(f"No parquet files found in {base_dir}")
        return

    for raw_data_path in parquet_files:
        # Extract base name
        file_stem = raw_data_path.stem
        output_parquet_path = base_dir / file_stem / "partitioned_market_orders"

        print(f"\n{'*'*50}")
        print(f"Processing File: {raw_data_path.name}")
        print(f"{'*'*50}")

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

if __name__ == "__main__":
    process_regional_partitions()
    print("\nAll region files have been successfully partitioned.")