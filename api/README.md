# Delivery Time Predictor API

A simple FastAPI service for predicting food delivery times using a trained ML model.

## Requirements
- Python 3.10+  
- A trained model file saved at the path defined in `model_pipeline/config.py` (`MODEL_PATH`).  

## Setup

1. **Clone the repository**

```bash
git clone git@github.com:jerry-whoami/pg-technical-assessment.git
cd pg-technical-assessment
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate # For linux
venv\Scripts\activate    # For Windows
```
3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Ensure model is available**

Generate the trained model file at the location specified by MODEL_PATH in model_pipeline/config.py.

```bash
python -m model_pipeline.pipeline
```

Run the API

Start the FastAPI server with Uvicorn:

```bash
uvicorn api.main:app --reload
```

- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Example Use Case

### Request

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
        "distance_km": 5.2,
        "preparation_time_min": 15,
        "courier_experience_yrs": 2,
        "weather": "Clear",
        "time_of_day": "Afternoon",
        "vehicle_type": "Bike",
        "traffic_level": "Medium"
      }'
```

### Respone

```bash
{
  "delivery_time_min": 32.4
}
```