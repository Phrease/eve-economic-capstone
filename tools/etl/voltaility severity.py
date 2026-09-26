import pandas as pd

df = pd.read_csv("C:/Users/durki/OneDrive/Desktop/MIS581/data/power_bi_data/did_analysis_data_1.csv")

# Scale variables down to billions to prevent SAS Viya memory overflow
df['total_trade_volume_billions'] = df['total_trade_volume'] / 1e9
df['calculated_destroyed_isk_blns'] = df['calculated_destroyed_isk'] / 1e9

# Define the bin edges in quantiles (33rd and 66th percentiles)
quantiles = df ['calculated_destroyed_isk'].quantile([0.33, 0.66]).to_dict()

def categorize_volatility(isk):
    if pd.isna(isk):
        return 'None' # Handles the sparse days with zero combat
    elif isk <= quantiles[0.33]:
        return 'Low'
    elif isk <= quantiles[0.66]:
        return 'Moderate'
    else:
        return 'Severe'

# Apply the function to create the new categorical target variable
df['volatility_severity'] = df['calculated_destroyed_isk'].apply(categorize_volatility)

# Filter out non-combat days
df_tree = df[df['volatility_severity'] != 'None']

# Save the updated dataset
df_tree.to_csv("C:/Users/durki/OneDrive/Desktop/MIS581/data/power_bi_data/did_analysis_data_cleaned_v1.csv", index=False)

print("Volatility bins generated. Target variable 'volatility_severity' added.")
print(df['volatility_severity'].value_counts())

print(df_tree.head())