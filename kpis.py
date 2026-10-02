import sqlite3
import pandas as pd

DB_PATH = "churn.db"

# Columns we allow for grouping (a fixed list, so nothing unexpected reaches the SQL)
ALLOWED_GROUPS = ["geography", "gender", "age_group", "num_of_products",
                  "is_active_member", "balance_band"]


def run_query(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def build_where(geographies=None, genders=None, age_groups=None, active=None):
    """Turn the dashboard filters into a WHERE clause plus a list of values."""
    clauses = []
    params = []
    filters = [
        ("geography", geographies),
        ("gender", genders),
        ("age_group", age_groups),
        ("is_active_member", active),
    ]
    for column, values in filters:
        if values:  # skip a filter if nothing is selected
            placeholders = ",".join("?" * len(values))
            clauses.append(f"{column} IN ({placeholders})")
            params.extend(values)
    where = "WHERE " + " AND ".join(clauses) if clauses else ""
    return where, params


def get_overview(where, params):
    """KPI 1, 3 and 5 headline numbers for the filtered customers."""
    query = f"""
    SELECT COUNT(*) AS total_customers,
           SUM(exited) AS churned,
           ROUND(100.0 * SUM(exited) / COUNT(*), 2) AS churn_rate_pct,
           ROUND(100.0 * SUM(is_active_member) / COUNT(*), 2) AS active_rate_pct,
           ROUND(100.0 * SUM(CASE WHEN exited = 1 THEN balance ELSE 0 END)
                 / SUM(balance), 2) AS balance_at_risk_pct
    FROM customers
    {where}
    """
    return run_query(query, params)


def get_segment_table(group_col, where, params):
    """KPI 2 and 4: churn rate, size and lift for any segment column."""
    if group_col not in ALLOWED_GROUPS:
        raise ValueError(f"Cannot group by {group_col}")
    query = f"""
    SELECT {group_col},
           COUNT(*) AS customers,
           SUM(exited) AS churned,
           ROUND(100.0 * SUM(exited) / COUNT(*), 2) AS churn_rate_pct
    FROM customers
    {where}
    GROUP BY {group_col}
    ORDER BY {group_col}
    """
    df = run_query(query, params)
    if not df.empty:
        overall = 100.0 * df["churned"].sum() / df["customers"].sum()
        df["lift"] = (df["churn_rate_pct"] / overall).round(2)
    return df