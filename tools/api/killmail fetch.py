import requests
import tarfile
import json
import pandas as pd
import os
from datetime import datetime
from tqdm import tqdm

def process_everef_dump(start_date="2026-01-01", end_date="2026-08-31", target_system=30000142):
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    date_list = pd.date_range(start, end).strftime('%Y-%m-%d').tolist()

    total_storage_bytes = 0

    for date_str in tqdm(date_list, desc="Fetching Killmails", unit="day"):
        url = f"https://data.everef.net/killmails/2026/killmails-{date_str}.tar.bz2"
        extracted_data = []

        print(f"Streaming and unpacking EVEREF data for {date_str}...")

        try:
            # Stream the request to avoid loading the entire archive
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                # Read the bz2 stream
                with tarfile.open(fileobj=r.raw, mode="r|bz2") as tar:
                    for member in tar:
                        if member.isreg() and member.name.endswith('.json'):
                            f = tar.extractfile(member)
                            if f:
                                kill = json.loads(f.read())

                                if kill.get('solar_system_id') == target_system:
                                    transaction_id = str(kill.get('killmail_id'))
                                    issued = kill.get('killmail_time')
                                    victim = kill.get('victim', {})

                                    if 'ship_type_id' in victim:
                                        extracted_data.append({
                                            'transaction_id': f"{transaction_id}_{victim['ship_type_id']}",
                                            'system_id': target_system,
                                            'issued': issued,
                                            'type_id': victim['ship_type_id'],
                                            'volume_total': 1,
                                            'destroyed_isk': None
                                        })

                                    for item in victim.get('items', []):
                                        if 'qty_destroyed' in item:
                                            extracted_data.append({
                                                'transaction_id': f"{transaction_id}_{item['item_type_id']}_{item.get('flag', 0)}",
                                                'system_id': target_system,
                                                'issued': issued,
                                                'type_id': item['item_type_id'],
                                                'volume_total': item['qty_destroyed'],
                                                'destroyed_isk': None
                                            })

            if extracted_data:
                df = pd.DataFrame(extracted_data)
                # Export to local directory
                output_path = os.path.expanduser(f"C:/Users/durki/OneDrive/Desktop/MIS581/data/combat_logs/everef_{date_str}.csv")
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                df.to_csv(output_path, index=False)

                # Calculating storage size
                file_size = os.path.getsize(output_path)
                total_storage_bytes += file_size

                #Setup Progress bar on extraction
                tqdm.write(f"Extraction complete: {len(df)} records saved to {output_path} ({file_size / 1024:.2f} KB)")
            else:
                tqdm.write(f"No combat logs found for system {target_system} on {date_str}.")

        except Exception as e:
            print(f"Failed to process {date_str}: {e}")

    # Total MBs
    total_storage_mb = total_storage_bytes / (1024 * 1024)
    print(f"\nTotal disk storage added: {total_storage_mb:.2f} MB")

process_everef_dump(start_date="2026-01-01", end_date="2026-08-31", target_system=30000142)