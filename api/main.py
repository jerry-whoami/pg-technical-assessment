from fastapi import FastAPI, HTTPException
from .schemas import PredictRequest, PredictResponse
from .service import predict

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
