import requests
import pandas as pd
from typing import List, Tuple, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

def discover_high_volume_structure(region_id: int, volume_threshold: int = 500) -> List[Tuple[int, int]]:
    """
    Fetches regional market orders, aggregates by location_id,
    and returns player structure IDs and their order counts exceeding the treshold.
    """
    base_url = f"https://esi.evetech.net/latest/markets/{region_id}/orders/"
    all_orders = []

    response = requests.get(base_url, params={"page": 1})
    response.raise_for_status()
    all_orders.extend(response.json())

    total_pages = int(response.headers.get("x-pages", 1))

    for page in range(2, total_pages + 1):
        resp = requests.get(base_url, params={"page": page})
        if resp.status_code == 200:
            all_orders.extend(resp.json())

    if not all_orders:
        return []

    df = pd.DataFrame(all_orders)

    structures_df = df[df['location_id'] >= 1_000_000_000_000]

    order_counts = structures_df.groupby('location_id').size().reset_index(name='order_count')

    high_volume_structures = order_counts[order_counts['order_count'] >= volume_threshold]

    high_volume_structures = high_volume_structures.sort_values(by='order_count', ascending=False)

    return list(high_volume_structures.itertuples(index=False, name=None))

def resolve_structure(structure_id: int, access_token: str) -> Optional[Dict]:
    """
    Resolves a 13-digit structure ID into its name and solar system ID.
    Requires an OAuth token with the esi-universe.read_structures.v1 scope.
    """
    url = f"https://esi.evetech.net/latest/universe/structures/{structure_id}/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return {
            "name": data.get("name"),
            "solar_system_id": data.get("solar_system_id")
        }
    return None

if __name__ == '__main__':
    target_region = 10000009
    threshold = 500
    my_token = os.getenv('ESO_TOKEN')

    print(f"Scanning region {target_region} for high-volume structures...")

    discovered_structures = discover_high_volume_structure(target_region, volume_threshold=threshold)

    if discovered_structures:
        print("Found the following structure IDs:")
        for struct_id, count in discovered_structures:
            resolved = resolve_structure(struct_id, my_token)
            if resolved:
                print(f"- {resolved['name']} (System ID: {resolved['solar_system_id']}) | ID: {struct_id} | Active Order: {count}")
            else:
                print(f"- Unknown Structure (Check Token/ACL) | ID: {struct_id} | Active Orders: {count}")

    else:
        print("No structures found exceeding the volume threshold.")