import pandas as pd

df = pd.read_csv("C:/Users/durki/OneDrive/Desktop/MIS581/data/region_10000002_orders.csv")

desc_stats = df.describe(include='all')
print(df.head())
print("\nDescriptive Statistics:\n")
print(desc_stats)