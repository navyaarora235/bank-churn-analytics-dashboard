import pandas as pd

pd.set_option("display.max_columns", None)

df = pd.read_csv("data/raw/Churn_Modelling.csv")

print("--- First 5 rows ---")
print(df.head())

print("\n--- Info (types and non-null counts) ---")
df.info()

print("\n--- Summary statistics ---")
print(df.describe())

print("\n--- Null values per column ---")
print(df.isnull().sum())

print("\n--- Duplicates ---")
print("Duplicate rows:", df.duplicated().sum())
print("Duplicate CustomerIds:", df["CustomerId"].duplicated().sum())

print("\n--- Target: Exited (1 = churned, 0 = stayed) ---")
print(df["Exited"].value_counts())

print("\n--- Geography ---")
print(df["Geography"].value_counts())

print("\n--- NumOfProducts ---")
print(df["NumOfProducts"].value_counts().sort_index())

print("\n--- Share of customers with zero balance ---")
print(round((df["Balance"] == 0).mean() * 100, 1), "%")