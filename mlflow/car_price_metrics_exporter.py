#!/usr/bin/env python3
"""
Car Price Prediction Metrics Exporter for Prometheus
Exposes car price prediction specific metrics in Prometheus format
"""

import os
import time
import psycopg2
import requests
from prometheus_client import start_http_server, Gauge, Counter, Histogram
from prometheus_client.core import REGISTRY

# Prometheus metrics for car price prediction
prediction_requests_total = Counter('car_price_prediction_requests_total', 'Total number of prediction requests', ['status', 'model_version'])
prediction_duration_seconds = Histogram('car_price_prediction_duration_seconds', 'Time spent on prediction', ['model_version'])
prediction_price_range = Histogram('car_price_prediction_price_range', 'Distribution of predicted prices', ['price_range'])
model_accuracy_score = Gauge('car_price_model_accuracy', 'Model accuracy score', ['model_version'])
model_last_updated = Gauge('car_price_model_last_updated_timestamp', 'Last model update timestamp', ['model_version'])

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'postgres'),
        port=os.getenv('POSTGRES_PORT', 5432),
        database=os.getenv('POSTGRES_DB', 'mlflow'),
        user=os.getenv('POSTGRES_USER', 'mlflow'),
        password=os.getenv('POSTGRES_PASSWORD', 'mlflow123')
    )

def collect_mlflow_metrics():
    """Collect metrics from MLflow database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get latest model run information
        cursor.execute("""
            SELECT 
                r.run_uuid,
                r.start_time,
                r.end_time,
                p.value as accuracy_score,
                rm.name as model_name,
                rm.creation_timestamp
            FROM runs r
            JOIN experiments e ON r.experiment_id = e.experiment_id
            LEFT JOIN params p ON r.run_uuid = p.run_uuid AND p.key = 'accuracy'
            LEFT JOIN registered_models rm ON rm.name LIKE '%car%price%'
            WHERE e.name LIKE '%car%price%'
            ORDER BY r.start_time DESC
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        if result:
            run_uuid, start_time, end_time, accuracy_score, model_name, creation_timestamp = result
            
            # Set model accuracy if available
            if accuracy_score:
                model_accuracy_score.labels(model_version=model_name or "unknown").set(float(accuracy_score))
            
            # Set last updated timestamp
            if creation_timestamp:
                model_last_updated.labels(model_version=model_name or "unknown").set(creation_timestamp.timestamp())
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error collecting MLflow metrics: {e}")

def collect_api_metrics():
    """Collect metrics from FastAPI application"""
    try:
        # Check API health
        response = requests.get("http://mlflow-fastapi-app-1:8005/", timeout=5)
        if response.status_code == 200:
            print("API is healthy")
    except Exception as e:
        print(f"API health check failed: {e}")

def collect_prediction_metrics():
    """Collect prediction-specific metrics"""
    try:
        # Simulate prediction request to collect metrics
        test_data = {
            "carname": "toyota camry",
            "wheelbase": 99.8,
            "carheight": 54.3,
            "horsepower": 102,
            "peakrpm": 5500,
            "citympg": 24,
            "fueltype": "gas",
            "aspiration": "std",
            "doornumber": "two",
            "carbody": "sedan",
            "drivewheel": "fwd",
            "enginelocation": "front",
            "enginetype": "ohc",
            "cylindernumber": "four",
            "fuelsystem": "mpfi"
        }
        
        start_time = time.time()
        response = requests.post(
            "http://mlflow-fastapi-app-1:8005/predict",
            json=test_data,
            timeout=10
        )
        duration = time.time() - start_time
        
        # Record prediction duration
        prediction_duration_seconds.labels(model_version="XGBoostRegressor").observe(duration)
        
        if response.status_code == 200:
            result = response.json()
            predicted_price = result.get("predicted_price", 0)
            
            # Categorize price range
            if predicted_price < 10000:
                price_range = "low"
            elif predicted_price < 25000:
                price_range = "medium"
            else:
                price_range = "high"
            
            prediction_price_range.labels(price_range=price_range).observe(predicted_price)
            prediction_requests_total.labels(status="success", model_version="XGBoostRegressor").inc()
        else:
            prediction_requests_total.labels(status="error", model_version="XGBoostRegressor").inc()
            
    except Exception as e:
        print(f"Error collecting prediction metrics: {e}")
        prediction_requests_total.labels(status="error", model_version="XGBoostRegressor").inc()

def main():
    """Main function"""
    print("Starting Car Price Prediction Metrics Exporter...")
    
    # Start Prometheus HTTP server
    start_http_server(8003)
    print("Car Price Prediction Metrics Exporter started on port 8003")
    
    # Collect metrics every 60 seconds
    while True:
        try:
            collect_mlflow_metrics()
            collect_api_metrics()
            collect_prediction_metrics()
            print("Metrics collected successfully")
        except Exception as e:
            print(f"Error in main loop: {e}")
        
        time.sleep(60)

if __name__ == "__main__":
    main()
