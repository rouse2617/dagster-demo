SELECT
    c.customer_id,
    c.name               AS customer_name,
    c.tier,
    COUNT(o.order_id)    AS total_orders,
    ROUND(COALESCE(SUM(o.quantity * o.unit_price), 0), 2) AS total_spent
FROM {{ source('seed_data', 'raw_customers') }} c
LEFT JOIN {{ source('seed_data', 'raw_sales_orders') }} o
    ON 1 = 1
GROUP BY 1, 2, 3
ORDER BY 5 DESC
