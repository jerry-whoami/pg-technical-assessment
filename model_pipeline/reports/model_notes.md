# Model Notes

## Modeling Goal

Predict **delivery_time_min** to improve ETA accuracy and support SLA planning. This is framed as a supervised regression problem.

## Why This Model

**Regression problem:** Target is continuous (minutes).
**XGBoost:** Performs well on structured/tabular data, handles nonlinear feature interactions, efficient at inference, and widely adopted in production.
**Tree-based method:** Naturally handles different scales, no need for feature normalization.

## Final Pipeline

- **Preprocessing:**
    - **Numeric:** Median imputation (`distance_km`, `preparation_time_min`, `courier_experience_yrs`).
    - **Categorical (nominal):** Most Frequent imputation and One-Hot Encoding for `weather`, `time_of_day`, `vehicle_type`.
    - **Categorical (ordinal):** Most Frequent imputation and Ordinal Encoding for `traffic_level` (Low < Medium < High).
- **Estimator:** XGBoost Regressor with `reg:absoluteerror` as objective metric.
- **Artifact:** Trained pipeline serialized with `joblib` at `model_pipeline/artifacts/model.pkl`.

## Training and Tuning Details

- **Objective**: `"reg:absoluteerror"` (optimizes MAE directly).
- **Train/validation split**: 80/20 random split, `random_state=7` for reproducibility.
- **Search strategy**: RandomizedSearchCV (50 iterations, 3-fold CV). Chosen over grid search for efficiency in exploring large hyperparameter spaces.
- **Hyperparameter ranges tested**:
  - `n_estimators`: 100–1000
  - `max_depth`: 3–10
  - `learning_rate`: 0.01–0.2
  - `subsample`: 0.8–1.0
  - `min_child_weight`: 1–10

> The ranges were chosen based on commonly recommended values from documentation and prior best practices.  

## Metrics

- **Primary metric**: MAE — directly interpretable as “average minutes off”. It also focuses on typical operations.
- **Secondary metrics**:
  - RMSE — penalizes large errors, useful for SLA risk.
  - R² — variance explained, check on overall fit.

## Validation Design

- Random train/test split, 20% holdout for testing.
- RandomizedSearchCV used 3-fold cross-validation within training for robust parameter tuning.
- Stratification not applied because target is continuous and evenly distributed.