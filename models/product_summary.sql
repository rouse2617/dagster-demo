SELECT
    product,
    COUNT(*)              AS total_orders,
    SUM(quantity)         AS total_quantity,
    ROUND(SUM(quantity * unit_price), 2) AS total_revenue,
    ROUND(AVG(unit_price), 2)            AS avg_unit_price
FROM {{ source('seed_data', 'raw_sales_orders') }}
GROUP BY 1
ORDER BY 2 DESC
