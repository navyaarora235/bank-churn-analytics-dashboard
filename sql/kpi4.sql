SELECT num_of_products,
       COUNT(*) AS customers,
       ROUND(100.0 * SUM(exited) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY num_of_products
ORDER BY num_of_products;