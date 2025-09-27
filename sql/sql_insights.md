# SQL Insights

## Key Insights from the Required Queries

| Section | Objective | Possible Insight |
|---------|-----------|------------------|
| Slowest Customer Areas | Identify top 5 customer areas with the highest average delivery time in the last 30 days | These areas consistently experience the longest delivery times. It is likely due to distance from restaurants or limited rider availability. We should research the cause in order to create a plan of action. |
| Delivery Time by Traffic & Cuisine | Compare average delivery times across traffic conditions, grouped by restaurant area and cuisine type | This comparison may reveal combinations of traffic conditions and cuisine types that generate delays. For example, cuisines with longer prep times for example Italian or Indian can be a major driver of delays. |
| Fastest Delivery People | Top 10 fastest riders, only active ones with 50 or more deliveries | Identifies consistently high-performing riders. We can then promote this behavior with recognition programs. |
| Most Profitable Restaurant Area  | Find the restaurant area with the highest total order value | Identifies areas that generate the most revenue, which would be key to prioritizing staffing and logistics. |
| Drivers Trending Slower | Detect drivers whose average delivery times are increasing over time | May show riders whose performance is declining, helping Ops decide where interventions like training or workload adjustments are needed. |

## 2. Additional Exploratory Questions

### Ratings vs Delivery Time

**Objective:** Average rating grouped into delivery time buckets.

**Possible Insight**: This could reveal how much customer satisfaction is affected by longer delivery times.

**Query:**

```sql
SELECT width_bucket(delivery_time_min, 0, 120, 6) AS time_bucket,
    ROUND(AVG(delivery_rating)::numeric, 2) AS avg_rating,
    COUNT(*) AS deliveries
FROM deliveries
GROUP BY time_bucket
ORDER BY time_bucket;
```

### Weather Impact

**Objective:** Average delivery time by weather condition.

**Possible Insight**: It can reflect how rain, storms, or fog affect delivery speed.

**Query:**

```sql
SELECT weather_condition,
    ROUND(AVG(delivery_time_min), 2) AS avg_delivery_time,
    COUNT(*) AS deliveries
FROM deliveries
GROUP BY weather_condition
ORDER BY avg_delivery_time DESC;
```

## Notes

- The database used for testing was postgresql with a small amount of sample data.
- __restaurant_area__ in __deliveries__ is treated as a regular column, not a foreign key, since it doesn’t follow the ___id__ naming convention used for identifiers.