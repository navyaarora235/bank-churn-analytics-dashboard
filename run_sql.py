import sqlite3
import sys
import pandas as pd

# Usage: python run_sql.py sql/kpi1.sql
sql_file = sys.argv[1]

with open(sql_file, "r") as f:
    query = f.read()

conn = sqlite3.connect("churn.db")
result = pd.read_sql_query(query, conn)
conn.close()

pd.set_option("display.max_columns", None)
print(result)