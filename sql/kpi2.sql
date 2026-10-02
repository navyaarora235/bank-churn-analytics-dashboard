SELECT geography,
       COUNT(*) AS customers,
       ROUND(100.0 * SUM(exited) / COUNT(*), 2) AS churn_rate_pct,
       ROUND((1.0 * SUM(exited) / COUNT(*)) /
             (SELECT 1.0 * SUM(exited) / COUNT(*) FROM customers), 2) AS lift
FROM customers
GROUP BY geography
ORDER BY churn_rate_pct DESC;