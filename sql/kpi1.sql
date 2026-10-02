SELECT COUNT(*) AS total_customers,
       SUM(exited) AS churned,
       ROUND(100.0 * SUM(exited) / COUNT(*), 2) AS churn_rate_pct
FROM customers;