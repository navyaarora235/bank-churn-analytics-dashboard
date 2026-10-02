import sqlite3
import pandas as pd

# 1. Read the clean CSV
df = pd.read_csv("data/clean/churn_clean.csv")

# 2. Connect to SQLite (creates churn.db if it doesn't exist)
conn = sqlite3.connect("churn.db")

# 3. Write the data to a table called 'customers' (replace it if it already exists)
df.to_sql("customers", conn, if_exists="replace", index=False)

# 4. Quick check: count the rows
row_count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
print("Rows in customers table:", row_count)

conn.close()