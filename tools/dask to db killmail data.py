import dask.dataframe as dd
from dask.diagnostics import ProgressBar
import pandas as pd
import psycopg2
import io
import os

# Target the EVEREF output
csv_path = os.path.expanduser("C:/Users/durki/OneDrive/Desktop/MIS581/data/combat_logs/everef_*.csv")
ddf = dd.read_csv(csv_path)

def transform_and_insert_everef(df, table_name, db_params):
    if df.empty:
        return 0

    # Synthesize missing dimensional data for combat telemetry
    df['event_category'] = 'Combat Killmail'
    df['price_isk'] = None
    df['is_buy_order'] = None

    # Generate the date_key integer
    df['issued'] = pd.to_datetime(df['issued'])
    df['date_key'] = df['issued'].dt.strftime('%Y%m%d').astype(int)

    ordered_columns = [
        'transaction_id', 'date_key', 'issued', 'is_buy_order',
        'type_id', 'system_id', 'price_isk', 'volume_total',
        'event_category', 'destroyed_isk'
    ]
    df = df[ordered_columns]

    # Drop duplicates to prevent PK conflicts
    df = df.drop_duplicates(subset=['transaction_id'])

    conn = psycopg2.connect(**db_params)
    sio = io.StringIO()

    df.to_csv(sio, index=False, header=False, na_rep='')
    sio.seek(0)

    with conn.cursor() as cursor:
        cursor.execute(f"CREATE TEMP TABLE temp_{table_name} (LIKE {table_name});")

        copy_query = f"""
            COPY temp_{table_name} (
            transaction_id, date_key, event_timestamp, is_buy_order,
            type_id, system_id, price_isk, volume_total,
            event_category, destroyed_isk
            ) FROM STDIN WITH CSV
        """
        cursor.copy_expert(sql=copy_query, file=sio)

        insert_query = f"""
            INSERT INTO {table_name}
            SELECT * FROM temp_{table_name}
            ON CONFLICT (transaction_id) DO NOTHING;
        """
        cursor.execute(insert_query)
        cursor.execute(f"DROP TABLE temp_{table_name}")

    conn.commit()
    conn.close()

    return len(df)

db_params = {
    'dbname': 'eve_economy',
    'user': 'postgres',
    'password': 'RmdSgn123456!',
    'host': 'localhost',
    'port': '5432'
}

write_tasks = ddf.map_partitions(
    transform_and_insert_everef,
    table_name='fact_market_events',
    db_params=db_params,
    meta=('row_count', 'i8')
)

print("Streaming EVEREF combat telemetry into PostgreSQL...")
with ProgressBar():
    total_inserted = write_tasks.sum().compute()

print(f"Successfully inserted {total_inserted} combat records.")