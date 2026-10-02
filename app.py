import streamlit as st
import plotly.express as px
from kpis import build_where, get_overview, get_segment_table

st.set_page_config(page_title="Bank Churn Analytics", layout="wide")
st.title("Bank Customer Churn Analytics")
st.caption("Snapshot of 10,000 bank customers. Churn rate = share of customers who exited.")

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")

geographies = st.sidebar.multiselect(
    "Country", ["France", "Germany", "Spain"],
    default=["France", "Germany", "Spain"])

genders = st.sidebar.multiselect(
    "Gender", ["Female", "Male"], default=["Female", "Male"])

age_groups = st.sidebar.multiselect(
    "Age group", ["18-30", "31-40", "41-50", "51-60", "60+"],
    default=["18-30", "31-40", "41-50", "51-60", "60+"])

activity = st.sidebar.selectbox("Member status", ["All", "Active", "Inactive"])
active_map = {"All": None, "Active": [1], "Inactive": [0]}

# Stop if any multiselect is empty (otherwise the filter would be skipped)
if not geographies or not genders or not age_groups:
    st.warning("Please select at least one option in Country, Gender and Age group.")
    st.stop()

# ---------- Build the WHERE clause and run the KPIs ----------
where, params = build_where(geographies, genders, age_groups, active_map[activity])
overview = get_overview(where, params).iloc[0]

# Overall numbers (no filters), used for comparison
overall = get_overview(*build_where()).iloc[0]

if overview["total_customers"] == 0:
    st.warning("No customers match these filters. Please widen your selection.")
    st.stop()

# ---------- KPI cards ----------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Customers", f"{int(overview['total_customers']):,}")
c2.metric("Churned", f"{int(overview['churned']):,}")

diff = overview["churn_rate_pct"] - overall["churn_rate_pct"]
c3.metric("Churn rate", f"{overview['churn_rate_pct']}%",
          delta=f"{diff:.2f} vs overall" if round(diff, 2) != 0 else None,
          delta_color="inverse")

c4.metric("Active-member rate", f"{overview['active_rate_pct']}%")
c5.metric("Balance at risk", f"{overview['balance_at_risk_pct']}%")

# ---------- Charts ----------
st.divider()
st.subheader("Where is churn highest?")


def churn_chart(group_col, title, label):
    df = get_segment_table(group_col, where, params)
    df[group_col] = df[group_col].astype(str)  # treat 0/1 and product counts as categories
    fig = px.bar(
        df, x=group_col, y="churn_rate_pct",
        text=df["churn_rate_pct"].astype(str) + "%",
        hover_data={"customers": True, "churned": True},
        title=title,
        labels={group_col: label, "churn_rate_pct": "Churn rate (%)"},
    )
    fig.add_hline(y=overview["churn_rate_pct"], line_dash="dash",
                  annotation_text="Selection average")
    fig.update_traces(textposition="outside")
    return fig


col1, col2 = st.columns(2)
col1.plotly_chart(churn_chart("geography", "Churn rate by country", "Country"),
                  width="stretch")
col2.plotly_chart(churn_chart("age_group", "Churn rate by age group", "Age group"),
                  width="stretch")

col3, col4 = st.columns(2)
col3.plotly_chart(churn_chart("num_of_products", "Churn rate by number of products",
                              "Number of products"), width="stretch")
col4.plotly_chart(churn_chart("is_active_member", "Churn rate: inactive (0) vs active (1)",
                              "Active member"), width="stretch")

col5, _ = st.columns(2)
col5.plotly_chart(churn_chart("balance_band", "Churn rate by balance band",
                              "Balance band"), width="stretch")

# ---------- Segment table ----------
st.divider()
st.subheader("Segment table: size, churn rate and lift")

segment_options = {
    "Country": "geography",
    "Gender": "gender",
    "Age group": "age_group",
    "Number of products": "num_of_products",
    "Member status (0 = inactive, 1 = active)": "is_active_member",
    "Balance band": "balance_band",
}
choice = st.selectbox("Segment by", list(segment_options.keys()))

seg = get_segment_table(segment_options[choice], where, params)
seg["share_of_customers_pct"] = (100.0 * seg["customers"] / seg["customers"].sum()).round(2)
seg["note"] = seg["customers"].apply(lambda n: "Small group: interpret with care" if n < 300 else "")
seg = seg.sort_values("lift", ascending=False)

st.dataframe(seg, hide_index=True, width="stretch")
st.caption("Lift = segment churn rate / churn rate of the current selection. "
           "Lift above 1 means the segment churns more than average.")