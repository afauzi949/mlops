from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from src.api import predict

app = FastAPI(
    title="Car Price Prediction API",
    description="API untuk memprediksi harga mobil berdasarkan fitur teknikal",
    version="1.0"
)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to Car Price Prediction API",
        "description": "API untuk memprediksi harga mobil berdasarkan fitur teknikal",
        "version": "1.0",
        "endpoints": {
            "docs": "/docs",
            "predict": "/predict",
            "metrics": "/metrics"
        },
        "usage": "Visit /docs for interactive API documentation"
    }

# Register router
app.include_router(predict.router)

# Monitoring endpoint: /metrics
Instrumentator().instrument(app).expose(app)
