# Strategic Reflections

## 1) **Model Failure:** Your model underestimates delivery time on rainy days. Do you fix the model, the data, or the business expectations?

**Answer:** The long term fix is adjust the **data** and the **model**. Meanwhile on the short term one should adjust **business expectations** temporarily.

### Recommended actions

- Increase rainy-day representation (reweight / oversample) to correct bias.  
- Add interaction signals likely driving the miss: `weather × traffic_level`, `weather × distance_km`.  
- Show ranges in rainy conditions while retraining.  

---

## 2) **Transferability:** The model performs well in Mumbai. It’s now being deployed in São Paulo. How do you ensure generalization?

**Answer:** Avoid assuming São Paulo looks like Mumbai. Treat it as **domain shift** and follow a staged deployment.

### Stages

- **Pre-deployment checks**
  - Run São Paulo dataset through the Mumbai model.
  - Compare errors (MAE, RMSE) across groups like weather and traffic.
  - Check feature distributions.

- **Adaption options**  
  - If the Mumbai model works decently in São Paulo, fine-tune it on local data.
  - If it doesn’t, then one should consider to train a country-aware or city-aware model where “country” or “city” is just another feature, so the model learns specific corrections while sharing general patterns.

- **Deployment**  
  - First run the model in **shadow mode**, where it makes predictions on live data but customers don’t see them. Once performance looks reliable, gradually roll it out to real users, starting small and expanding as results stay accurate.

---

## 3) GenAI Disclosure: Generative AI tools are a great resource that can facilitate development, what parts of this project did you use GenAI tools for? How did you validate or modify their output?

### GenAI Use Cases

- **Documentation**: Drafted READMEs and markdowns, suggested boilerplate sections, and polished drafts into a professional style.  
- **Code scaffolding**: Generated boilerplate for the API, ML pipeline, hyperparameter tuning, and a Postgres test database.  
- **Data & analysis**: Produced visualizations (matplotlib, seaborn), reviewed SQL queries, and validated feature engineering / training code.

### Validation and Modifications

All AI-generated output was verified before use:  

- Cross-checked with official documentation and trusted references.  
- Executed locally to confirm correctness.  
- Simplified when content was overly complex.  
- Edited or replaced when outdated, incorrect, or not aligned with best practices.  

---

## 4) Your Signature Insight

**Answer:** While most examples used one-hot encoding for `traffic_level`, I treated it as an **ordinal feature** (Low < Medium < High). This matched the natural order of congestion, gave the model cleaner splits, and improved accuracy without adding unnecessary complexity.  

---

## 5) Going to Production

### How would you deploy your model to production? 

### 5.1 Problem Formulation  

- State clearly the business problem one wants to solve: Predict delivery times accurately to improve ETAs and operational efficiency.  
- Establish success metrics: MAE within tolerance (e.g., ±5 minutes), API latency <200 ms, uptime ≥99.9%.  
- Define constraints such as data sources and infrastructure available. For example, deployment must run in containerized cloud with autoscaling.  

### 5.2 Architecture  

- Use model registry and artifact storage for versioning, reproducibility, and rollback.  
- Define how inferences will be computed: batch scoring for analytics, real-time API for live ETAs behind a load balancer with autoscaling.  
- Use an observability stack to evaluate performance, latency, errors, and detect data drift with alerts.  

### 5.3 Training  

- Checks on all inputs/labels including schema, range, and enum validation.  
- Set up a reproducible pipeline with preprocessing, training, evaluation, and artifact storage.  
- Register models with metadata (metrics, schema, training data snapshot) for reproducibility and safe promotion.  

### 5.4 Testing  

- Unit tests for preprocessing and model logic.  
- Integration tests for API endpoints and batch jobs.  
- Load tests to verify latency and stability under traffic.  
- Contract tests to ensure schema compatibility over time.  

### 5.5 Deployment  

- Containerize the application with the trained model artifact.  
- Deploy behind load balancer with autoscaling policies in case of live inferences.
- Use canary strategy for rolling out new versions safely.  
- Maintain rollback procedures to revert to the last stable release.  

### 5.6 Monitoring & Maintenance  

- Track infrastructure health (CPU, memory), API health (latency, error rates), and model health (MAE, drift).  
- Trigger alerts when thresholds are breached.  
- Schedule retraining when drift or performance degradation is detected.  
- Review costs and optimize resource allocation periodically.  

### What other components would you need to include/develop in your codebase?

#### Components needed to be included

- **API service**: real-time `/predict` endpoint plus batch job support; health and version endpoints.  
- **Model registry & storage**: keep model binaries, preprocessing pipeline, metrics, and schema; enable versioning and rollback.  
- **Training pipeline**: reproducible workflow with data validation, preprocessing, training, evaluation, and artifact logging.  
- **Data validation**: schema, range, and enum checks at both training and inference stages.  
- **Testing suite**: unit, integration, load, and contract tests to ensure reliability and compatibility.  
- **Observability**: monitor latency, error rates, drift, and resource use; set alerts for breaches.  
- **CI/CD**: automated pipelines for training, testing, deployment, and safe promotion.  
- **Deployment & rollout**: containerized service with autoscaling, load balancer, and canary/blue-green rollout strategies.  
- **Security & compliance**: secrets management, authentication, encryption, and minimal PII handling.  
- **Documentation & runbooks**: API/data contract, on-call guides, and rollback procedures.  

#### Components that have already been prototyped

- **API service**: Basic `/predict` and `/health` endpoints implemented to serve predictions and verify service availability.  

```py
# main.py
app = FastAPI(
    title="Delivery Time Predictor",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict_endpoint(req: PredictRequest):
    try:
        y = predict(req)
        return PredictResponse(delivery_time_min=y)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Inference failed: {e}")
```

- **Training pipeline**: End-to-end workflow covering preprocessing, training, and evaluation; currently outputs only the model file as an artifact. Data validation for new datasets must be implemented.

```py
NUM_COLS = ["Distance_km", "Preparation_Time_min", "Courier_Experience_yrs"]
CAT_ONEHOT_COLS = ["Weather", "Time_of_Day", "Vehicle_Type"]
CAT_ORDINAL_COLS = ["Traffic_Level"]


def build_preprocessor():
    num = Pipeline([
        ("imputer", SimpleImputer(strategy="median"))
    ])

    cat_onehot = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    cat_ordinal = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("ord", OrdinalEncoder(categories=[["Low","Medium","High"]]))
    ])

    pre = ColumnTransformer(
        transformers=[
            ("num", num, NUM_COLS),
            ("cat_oh", cat_onehot, CAT_ONEHOT_COLS),
            ("cat_ord", cat_ordinal, CAT_ORDINAL_COLS),
        ],
        remainder="drop"
    )

    return pre


def train():
    df = pd.read_csv(DATA_PATH)

    y = df[TARGET].values
    X = df.drop(columns=[TARGET])

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=TEST_SIZE, random_state=SEED)

    pre = build_preprocessor()

    model = XGBRegressor(
        objective="reg:absoluteerror",
        n_estimators=700,
        learning_rate=0.0311,
        max_depth=3,
        subsample=1.0,
        min_child_weight=9,
        random_state=SEED,
        n_jobs=4
    )

    pipe = Pipeline([
        ("pre", pre),
        ("model", model)
    ])

    pipe.fit(X_train, y_train)
    
    joblib.dump(pipe, MODEL_PATH)

    return MODEL_PATH


def evaluate():
    df = pd.read_csv(DATA_PATH)
    y = df[TARGET].values
    X = df.drop(columns=[TARGET])

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=TEST_SIZE, random_state=SEED)

    pipe = joblib.load(MODEL_PATH)
    y_pred = pipe.predict(X_val)

    mae = mean_absolute_error(y_val, y_pred)
    rmse = root_mean_squared_error(y_val, y_pred)
    r2 = r2_score(y_val, y_pred)

    print(f"MAE : {mae:.2f} min")
    print(f"RMSE: {rmse:.2f} min")
    print(f"R²  : {r2:.3f}")

if __name__ == "__main__":
    path = train()
    print(f"Saved model to {path}")

    evaluate()
```

- **Data validation**: Initial schema, range, and enum checks integrated for inference data with the API. Should include an initial step to validate the data at the start of the pipeline

```py
class Weather(str, Enum):
    clear = "Clear"
    rainy = "Rainy"
    snowy = "Snowy"
    foggy = "Foggy"
    windy = "Windy"

class TimeOfDay(str, Enum):
    morning = "Morning"
    afternoon = "Afternoon"
    evening = "Evening"
    night = "Night"

class VehicleType(str, Enum):
    bike = "Bike"
    scooter = "Scooter"
    car = "Car"

class TrafficLevel(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class PredictRequest(BaseModel):
    distance_km: Annotated[float, Field(description="Distance in kilometers")]
    preparation_time_min: Annotated[int, Field(description="Restaurant prep time in minutes")]
    courier_experience_yrs: Annotated[float, Field(description="Courier experience in years")]
    weather: Weather
    time_of_day: TimeOfDay
    vehicle_type: VehicleType
    traffic_level: TrafficLevel

class PredictResponse(BaseModel):
    delivery_time_min: float

```

- **Documentation & runbooks**: Minimal setup guide included to explain how to run the prototype and its components.  

```txt
api/README.md
sql/test_database/README.md
README.md
```