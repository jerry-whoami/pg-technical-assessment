-- 1. Top 5 customer areas with highest average delivery time in the last 30 days.
SELECT customer_area,
    ROUND(AVG(delivery_time_min), 2) AS avg_delivery_time_min
FROM deliveries
WHERE order_placed_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY customer_area
ORDER BY avg_delivery_time_min DESC
LIMIT 5;

-- 2. Average delivery time per traffic condition, by restaurant area and cuisine type.
SELECT d.traffic_condition, 
    d.restaurant_area, 
    r.cuisine_type, 
    ROUND(AVG(d.delivery_time_min), 2) AS avg_delivery_time_min
FROM deliveries AS d
JOIN restaurants AS r ON d.restaurant_area = r.area
GROUP BY d.traffic_condition, d.restaurant_area, r.cuisine_type;

-- 3. Top 10 delivery people with the fastest average delivery time, considering only those with at least 50 deliveries and who are still active.
SELECT p.delivery_person_id,
    p.name,
    ROUND(AVG(d.delivery_time_min), 2) AS avg_delivery_time_min,
    COUNT(*) AS total_deliveries
FROM delivery_persons AS p
JOIN deliveries AS d ON p.delivery_person_id = d.delivery_person_id
WHERE p.is_active = TRUE
GROUP BY p.delivery_person_id, p.name
HAVING COUNT(*) >= 50
ORDER BY avg_delivery_time_min DESC
LIMIT 10;

-- 4. The most profitable restaurant area in the last 3 months, defined as the area with the highest total order value.
SELECT r.area,
    ROUND(SUM(o.order_value)::numeric, 2) AS total_order_value,
    COUNT(*) AS orders_count
FROM orders o
JOIN deliveries d ON o.delivery_id = d.delivery_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE order_placed_at >= CURRENT_DATE - INTERVAL '3 months'
GROUP BY r.area
ORDER BY total_order_value DESC, orders_count DESC
LIMIT 1;

-- 5. Identify whether any delivery people show an increasing trend in average delivery time.
-- Create monthly averages for each driver
WITH monthly AS (
    SELECT d.delivery_person_id,
        date_trunc('month', d.order_placed_at)::date AS month,
        AVG(d.delivery_time_min) AS avg_time
    FROM deliveries d
    GROUP BY d.delivery_person_id, month
),
-- Normalize the driver's monthly average
-- This is done to identify who is getting slower compared to their usual speed
normalized AS (
    SELECT delivery_person_id,
        ROW_NUMBER() OVER (PARTITION BY delivery_person_id ORDER BY month) AS month_number,
        1.0 * avg_time / AVG(avg_time) OVER (PARTITION BY delivery_person_id) AS normalized_avg_time
    FROM monthly
)
-- Calculate a linear regression on the data and return any positive trend
SELECT delivery_person_id,
    REGR_SLOPE(normalized_avg_time, month_number) AS slope,
    COUNT(*) AS months_observed
FROM normalized
GROUP BY delivery_person_id
HAVING REGR_SLOPE(normalized_avg_time, month_number) > 0
ORDER BY slope DESC;