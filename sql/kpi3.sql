SELECT is_active_member,
       COUNT(*) AS customers,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customers), 2) AS share_pct,
       ROUND(100.0 * SUM(exited) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY is_active_member;