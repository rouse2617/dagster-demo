SELECT
    DATE(ordered_at)                  AS order_date,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(DISTINCT order_id)          AS order_count
FROM {{ source('seed_data', 'raw_sales_orders') }}
GROUP BY 1
ORDER BY 1
