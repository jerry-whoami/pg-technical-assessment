import pandas as pd
from api.schemas import PredictRequest
from model_pipeline.config import MODEL_PATH
from functools import lru_cache
import joblib

_INPUT_COLUMNS = [
    "Distance_km",
    "Preparation_Time_min",
    "Courier_Experience_yrs",
    "Weather",
    "Time_of_Day",
    "Vehicle_Type",
    "Traffic_Level",
]

@lru_cache(maxsize=1)
def _get_model():
    return joblib.load(MODEL_PATH)

def predict(payload: PredictRequest) -> float:
    model = joblib.load(MODEL_PATH)

    row = pd.DataFrame([{
        "Distance_km": payload.distance_km,
        "Preparation_Time_min": payload.preparation_time_min,
        "Courier_Experience_yrs": payload.courier_experience_yrs,
        "Weather": payload.weather.value,
        "Time_of_Day": payload.time_of_day.value,
        "Vehicle_Type": payload.vehicle_type.value,
        "Traffic_Level": payload.traffic_level.value,
    }], columns=_INPUT_COLUMNS)

    y_pred = model.predict(row)

    return float(y_pred[0])