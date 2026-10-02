# KPI Definitions

Data: 10,000 bank customers, one snapshot with no dates. "Churn rate" here is the share of customers in the file who exited, not a monthly rate.

## KPI 1: Churn rate
- **Formula:** churned customers / total customers (2,037 / 10,000 = 20.37%)
- **Grain:** all customers
- **Why it matters:** the headline retention metric; every other KPI explains movement in it.
- **Caveat:** snapshot only, so no trend over time.

## KPI 2: Segment churn rate and lift
- **Formula:** segment churn rate / overall churn rate (Germany: 32.44 / 20.37 = 1.59)
- **Grain:** one row per segment (geography, age group, gender)
- **Why it matters:** shows where to focus retention effort.
- **Caveat:** small segments give noisy rates, so segment size is always shown next to the rate.

## KPI 3: Active-member rate and churn gap
- **Formula:** active customers / total (51.51%); churn gap = inactive churn rate - active churn rate (26.85 - 14.27 = 12.58 points)
- **Grain:** active vs inactive customers
- **Why it matters:** engagement is an early warning sign, so re-activation is a clear product lever.
- **Caveat:** inactivity may be a symptom of leaving, not only a cause.

## KPI 4: Churn by number of products
- **Formula:** churn rate for each product count (1, 2, 3, 4)
- **Grain:** one row per product count
- **Why it matters:** tests whether cross-selling helps retention.
- **Caveat:** correlation only. The 3 and 4 product groups are tiny (266 and 60 customers), so their rates are unreliable.

## KPI 5: Balance at risk
- **Formula:** total balance of churned customers / total balance of all customers (24.26%)
- **Grain:** all customers
- **Why it matters:** churn rate treats every customer equally; this weights churn by money.
- **Caveat:** 36.2% of customers have zero balance, and a few large accounts can dominate the total.