import os
import pandas as pd

# 1. Load raw data
df = pd.read_csv("data/raw/Churn_Modelling.csv")
print("Raw shape:", df.shape)

# 2. Drop columns with no analytic value (RowNumber = index, Surname = personal data)
df = df.drop(columns=["RowNumber", "Surname"])

# 3. Rename columns to snake_case
df = df.rename(columns={
    "CustomerId": "customer_id",
    "CreditScore": "credit_score",
    "Geography": "geography",
    "Gender": "gender",
    "Age": "age",
    "Tenure": "tenure",
    "Balance": "balance",
    "NumOfProducts": "num_of_products",
    "HasCrCard": "has_cr_card",
    "IsActiveMember": "is_active_member",
    "EstimatedSalary": "estimated_salary",
    "Exited": "exited",
})
# 3b. Engineered columns
df["age_group"] = pd.cut(
    df["age"],
    bins=[17, 30, 40, 50, 60, 120],
    labels=["18-30", "31-40", "41-50", "51-60", "60+"],
)

df["balance_band"] = pd.cut(
    df["balance"],
    bins=[-1, 0, 100000, 150000, float("inf")],
    labels=["Zero", "Under 100k", "100k-150k", "150k+"],
)

# Store as plain text so SQLite and Streamlit handle them without surprises
df["age_group"] = df["age_group"].astype(str)
df["balance_band"] = df["balance_band"].astype(str)

# 4. Validation checks (the script stops with an error if any fails)
assert df.isnull().sum().sum() == 0, "Found null values"
assert df["customer_id"].is_unique, "Found duplicate customer IDs"
assert df["exited"].isin([0, 1]).all(), "exited must be 0 or 1"
assert df["is_active_member"].isin([0, 1]).all(), "is_active_member must be 0 or 1"
assert df["age_group"].ne("nan").all(), "Some ages were not assigned to a group"
assert df["balance_band"].ne("nan").all(), "Some balances were not assigned to a band"
print("All validation checks passed")

# 5. Save the clean file
os.makedirs("data/clean", exist_ok=True)
df.to_csv("data/clean/churn_clean.csv", index=False)

print("Clean shape:", df.shape)
print(list(df.columns))