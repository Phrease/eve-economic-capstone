import requests
import pandas as pd
import time
from pathlib import Path

def pull_regional_market_data(region_id):
    """
    Pulls all active buy and sell orders for a specific region from EVE ESI.
    """
    url = f"https://esi.evetech.net/latest/markets/{region_id}/orders/"

    headers = {
        "User-Agent": "Capstone-Project - Macro/Micro Analytics",
        "Accept": "application/json"
    }

    params = {
        "datasource": "tranquility",
        "order_type": "all",
        "page": 1
    }

    print(f"Fetching page 1 for Region {region_id}...")
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    orders = response.json()

    total_pages = int(response.headers.get("X-pages", 1))
    print(f"Total pages detected: {total_pages}")

    for page in range(2, total_pages + 1):
        params["page"] = page
        print(f"Fetching page {page} of {total_pages}...")

        res = requests.get(url, headers=headers, params=params)

        if res.status_code == 200:
            orders.extend(res.json())
        else:
            print(f"Failed to fetch page {page}. HTTP Status: {res.status_code}")

            time.sleep(0.05)

    return pd.DataFrame(orders)

if __name__ == "__main__":
    # Directory of target regions and their corresponding ESI Region IDs
    target_regions = {
        "The Forge": 10000002,
        "Heimatar": 10000030,
        "Sinq Laison": 10000032,
        "Domain": 10000043
    }

    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir.parent.parent / "data"

    # Ensuring data directory exists
    data_dir.mkdir(parents=True, exist_ok=True)

    for region_name, region_id in target_regions.items():
        print(f"\n Processing {region_name} (Region ID: {region_id})")

        df_market = pull_regional_market_data(region_id)
        print(f"Total orders retrieve for {region_name}: {len(df_market)}")

        # Save each region to its own parquet file
        output_filename = data_dir / f"region_{region_name}_{region_name.replace(' ', '_')}_orders.parquet"
        print(f"Saving to {output_filename}...")
        df_market.to_parquet(output_filename, engine="pyarrow", index=False)

    print("\nComplete")