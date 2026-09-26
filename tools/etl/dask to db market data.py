import dask.dataframe as dd
from dask.diagnostics import ProgressBar
import pandas as pd
import psycopg2
import io
import os
from dotenv import load_dotenv

load_dotenv()

base_dir = "C:/Users/durki/OneDrive/Desktop/MIS581/data"
regions = [
    "region_10000002_orders",
    "region_10000030_orders",
    "region_10000032_orders",
    "region_10000043_orders"
]

parquet_paths = [os.path.expanduser(f"{base_dir}/{region}/partitioned_market_orders/**/*.parquet") for region in regions]

# Ingest the Parquet dataset
ddf = dd.read_parquet(parquet_paths, engine='pyarrow')

# Defining the transformation and COPY execution function for each partition
def transform_and_insert (df, table_name, db_params):
    if df.empty:
        return 0

    # Synthesize missing schema columns for market order telemetry
    df['event_category'] = 'Market Order'
    df['destroyed_isk'] = None

    # Rename ESI columns to match column types
    df = df.rename(columns={'order_id': 'transaction_id', 'price': 'price_isk'})

    # Generate the date_key (YYYYMMDD) integer for datetime column
    df['issued'] = pd.to_datetime(df['issued'])
    df['date_key'] = df['issued'].dt.strftime('%Y%m%d').astype(int)

    # Reorder columns to map to table schema
    ordered_columns = [
        'transaction_id',
        'date_key',
        'issued',
        'is_buy_order',
        'type_id',
        'system_id',
        'price_isk',
        'volume_total',
        'event_category',
        'destroyed_isk'
    ]
    df = df[ordered_columns]

    df = df.drop_duplicates(subset=['transaction_id'])

    # Connect to local database
    conn = psycopg2.connect(**db_params)
    sio = io.StringIO()

    # Write df to the in-memory buffer without index or headers
    df.to_csv(sio, index=False, header=False, na_rep='')
    sio.seek(0)

    with conn.cursor() as cursor:
        # Create temp staging table modeled after the fact table
        cursor.execute(f"CREATE TEMP TABLE temp_{table_name} (LIKE {table_name});")

        # Copy the data from the memory buffer into the temp table
        copy_query = f"""
            COPY temp_{table_name} (
            transaction_id, date_key, event_timestamp, is_buy_order,
            type_id, system_id, price_isk, volume_total,
            event_category, destroyed_isk
            ) FROM STDIN WITH CSV
        """
        cursor.copy_expert(sql=copy_query, file=sio)

        # Insert unique records into the target table, ignoring duplicate PKs
        insert_query = f"""
            INSERT INTO {table_name}
            SELECT * FROM temp_{table_name}
            ON CONFLICT (transaction_id) DO NOTHING;
        """
        cursor.execute(insert_query)

        # Drop temp table    
        cursor.execute(f"DROP TABLE temp_{table_name};")

        conn.commit()
        conn.close()

        return len(df)

# Configure local db credentials
db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Map the pipeline function across all Dask partitions
write_tasks = ddf.map_partitions(
    transform_and_insert,
    table_name='fact_market_events',
    db_params=db_params,
    meta=('row_count', 'i8')
)

# Execute load
print("Streaming partitioned Parquet data into PostgreSQL...")
with ProgressBar():
    total_inserted = write_tasks.sum().compute()

print(f"Successfully inserted {total_inserted} rows.")