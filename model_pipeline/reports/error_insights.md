# Error Insights

## Goal

Analyze residuals (actual – predicted) to identify when and why the model underperforms, and highlight cases where errors are largest.

## Key Insights

- **Distance**: Errors grow with trip length. Deliveries beyond 5 km are consistently underestimated, with variance exploding on 10+ km routes.  
- **Weather**: Adverse conditions (Foggy, Rainy, Windy) inflate errors by several minutes. Snowy deliveries are the odd case — often overestimated.  
- **Traffic**: Medium and Low traffic settings show larger residuals than High traffic, suggesting the model under-corrects for lighter congestion.  
- **Vehicle type**: Scooters give the most stable predictions. Cars, on the other hand, are tied to the largest underestimations.  
- **Worst offenders**: The top 5 misses all involve long trips plus adverse conditions, with errors as high as 60+ minutes.  

## Residual Analysis

### By Distance

- Short trips (0–5 km): Residuals are near zero on average; predictions are accurate.
- Longer trips (5–10 km, 10+ km): Errors increase, with mean residuals of +2–3 minutes, showing underestimation of long-distance deliveries.
- Variance also grows with distance, confirming higher uncertainty in longer routes.

### By Preparation Time

- Short prep times (<5 min): Residuals close to zero.
- Longer prep times (>10 min): Mean residual ≈ +2.7 minutes with higher variance, suggesting the model underestimates orders with unusually long preparation.

### By Weather

- Clear weather: Residuals small and stable (+0.9 min).
- Foggy, Rainy, Windy: Higher mean errors (+1.8 to +7.3 min), showing the model struggles in adverse conditions.
- Snowy: Negative mean residual (–2.9 min), indicating overestimation under snow, though sample size is small.

### By Vehicle Type

- Scooters: Lowest residuals (~+0.6 min, lowest variance).
- Bikes: Small positive bias (~+1.0 min).
- Cars: Highest mean residual (+4.3 min), underestimation is stronger, especially in congested settings.

### By Traffic Level

- Low traffic: Residuals inflated (+3.5 min mean), high variance.
- Medium traffic: Highest average error (+1.8 min).
- High traffic: Lower average residuals (+0.7 min), though errors still present.

## Representative Failure Cases

The five largest errors occurred on long trips with adverse conditions:

1. **Distance 18 km, Clear weather, Car** — underpredicted by 62 minutes.
2. **Distance 19 km, Foggy weather, Car** — underpredicted by 58 minutes.
3. **Distance 7 km, Rainy weather, Car** — underpredicted by 41 minutes.
4. **Distance 7 km, Foggy weather, Scooter** — underpredicted by 37 minutes.
5. **Distance 16 km, Rainy weather, Bike** — underpredicted by 31 minutes.

> Common themes: long distances and adverse weather.

## Remediation Options

- **Feature engineering**: Add interaction features (`distance × traffic`, `weather × traffic`) to capture joint effects.
- **Data balancing**: Oversample adverse weather cases to reduce bias toward clear conditions.