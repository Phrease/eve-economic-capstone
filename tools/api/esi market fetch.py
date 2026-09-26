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
    target_region = 10000002

    df_market = pull_regional_market_data(target_region)
    print(f"\nTotal orders retrieved: {len(df_market)}")
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir.parent.parent / "data"

    output_filename = data_dir / f"region_{target_region}_orders.parquet"
    print(f"Saving to {output_filename}...")
    df_market.to_parquet(output_filename, engine="pyarrow", index=False)
    print("Complete")