import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from kpis import run_query

st.set_page_config(page_title="Churn Drivers", layout="wide")
st.title("What is linked to churn?")
st.caption("Logistic Regression used only to explain drivers, not to predict. "
           "It uses all 10,000 customers and ignores the sidebar filters.")

df = run_query("SELECT * FROM customers")

# Build the feature table with readable names
X = pd.DataFrame({
    "Age": df["age"],
    "Tenure": df["tenure"],
    "Balance": df["balance"],
    "Credit score": df["credit_score"],
    "Estimated salary": df["estimated_salary"],
    "Active member": df["is_active_member"],
    "Has credit card": df["has_cr_card"],
    "Male": (df["gender"] == "Male").astype(int),
    "Germany (vs France)": (df["geography"] == "Germany").astype(int),
    "Spain (vs France)": (df["geography"] == "Spain").astype(int),
    "3+ products": (df["num_of_products"] >= 3).astype(int),
})

# Standardize the numeric columns so their coefficients are comparable
num_cols = ["Age", "Tenure", "Balance", "Credit score", "Estimated salary"]
X[num_cols] = StandardScaler().fit_transform(X[num_cols])

model = LogisticRegression(max_iter=1000).fit(X, df["exited"])

drivers = pd.DataFrame({
    "Factor": X.columns,
    "Coefficient": model.coef_[0].round(3),
    "Odds ratio": np.exp(model.coef_[0]).round(2),
}).sort_values("Coefficient")

fig = px.bar(drivers, x="Coefficient", y="Factor", orientation="h",
             title="Effect on churn (right = more churn, left = less churn)")
st.plotly_chart(fig, width="stretch")

st.dataframe(drivers.sort_values("Coefficient", ascending=False),
             hide_index=True, width="stretch")

st.markdown("""
**How to read this**
- **Coefficient above 0** means the factor is linked to higher churn, below 0 to lower churn.
- **Odds ratio** = e^coefficient. An odds ratio of 2 means the odds of churning are about twice as high.
- **Age, Tenure, Balance, Credit score and Salary** are standardized, so the odds ratio is per 1 standard deviation increase.
- **Yes/no factors** (Active member, Germany, 3+ products) compare against the other group, holding everything else fixed.

**Caveats**
- These are associations, not causes.
- Number of products is not a straight line (2 products churn least, 1 and 3+ churn more), so it is shown as a 3+ products flag.
- Coefficients can shift if related factors, such as age and balance, overlap.
""")