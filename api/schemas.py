from enum import Enum
from pydantic import BaseModel, Field
from typing import Annotated

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
