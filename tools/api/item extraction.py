import pandas as pd
import os

# Specific item IDs that were missing
missing_ids = [97249, 97314, 97263, 97246, 97247]

print("Downloading static item data...")
df_types = pd.read_csv("https://www.fuzzwork.co.uk/dump/latest/csv/invTypes.csv")
df_groups = pd.read_csv("https://www.fuzzwork.co.uk/dump/latest/csv/invGroups.csv")
df_categories = pd.read_csv("https://www.fuzzwork.co.uk/dump/latest/csv/invCategories.csv")

# Merge types to groups for the categoryID
df_merged = pd.merge(df_types, df_groups[['groupID', 'categoryID']], on='groupID', how='left')

# Merge categories to extract the exact categoryName string
df_full = pd.merge(df_merged, df_categories[['categoryID', 'categoryName']], on='categoryID', how='left')

# Format the df to match the schema
dim_item = df_full[['typeID', 'typeName', 'categoryName']].copy()
dim_item.columns = ['type_id', 'item_name', 'item_category']

# Fill any missing items to prevent database insertion errors
dim_item['item_category'] = dim_item['item_category'].fillna('Unclassified')

# Isolate only the missing records
missing_records = dim_item[dim_item['type_id'].isin(missing_ids)]
print(f"Found {len(missing_records)} matching items to append.")

csv_path = os.path.expanduser("C:/Users/durki/OneDrive/Desktop/MIS581/data/dim_item.csv")
dim_item.to_csv(csv_path, index=False)
print(f"Item mapping saved to {csv_path}")