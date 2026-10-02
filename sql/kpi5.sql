SELECT ROUND(SUM(CASE WHEN exited = 1 THEN balance ELSE 0 END), 0) AS churned_balance,
       ROUND(100.0 * SUM(CASE WHEN exited = 1 THEN balance ELSE 0 END) / SUM(balance), 2) AS balance_at_risk_pct,
       ROUND(AVG(CASE WHEN exited = 1 THEN balance END), 0) AS avg_balance_churned,
       ROUND(AVG(CASE WHEN exited = 0 THEN balance END), 0) AS avg_balance_retained
FROM customers;