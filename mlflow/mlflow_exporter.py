#!/usr/bin/env python3
"""
MLflow Exporter for Prometheus
Exposes MLflow metrics in Prometheus format
"""

import os
import time
import psycopg2
from prometheus_client import start_http_server, Gauge, Counter, Histogram
from prometheus_client.core import REGISTRY

# Prometheus metrics
mlflow_runs_total = Counter('mlflow_runs_total', 'Total number of MLflow runs', ['experiment_name'])
mlflow_models_total = Counter('mlflow_models_total', 'Total number of MLflow models', ['experiment_name'])
mlflow_artifacts_total = Counter('mlflow_artifacts_total', 'Total number of MLflow artifacts', ['experiment_name'])
mlflow_experiments_total = Gauge('mlflow_experiments_total', 'Total number of MLflow experiments')

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'postgres'),
        port=os.getenv('POSTGRES_PORT', 5432),
        database=os.getenv('POSTGRES_DB', 'mlflow'),
        user=os.getenv('POSTGRES_USER', 'mlflow'),
        password=os.getenv('POSTGRES_PASSWORD', 'mlflow123')
    )

def collect_metrics():
    """Collect metrics from MLflow database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Count experiments
        cursor.execute("SELECT COUNT(*) FROM experiments")
        experiments_count = cursor.fetchone()[0]
        mlflow_experiments_total.set(experiments_count)
        
        # Count runs per experiment
        cursor.execute("""
            SELECT e.name, COUNT(r.run_uuid) 
            FROM experiments e 
            LEFT JOIN runs r ON e.experiment_id = r.experiment_id 
            GROUP BY e.experiment_id, e.name
        """)
        
        for experiment_name, run_count in cursor.fetchall():
            mlflow_runs_total.labels(experiment_name=experiment_name).inc(run_count)
        
        # Count models per experiment
        cursor.execute("""
            SELECT e.name, COUNT(DISTINCT rm.name) 
            FROM experiments e 
            LEFT JOIN runs r ON e.experiment_id = r.experiment_id 
            LEFT JOIN registered_models rm ON rm.name LIKE '%' || e.name || '%'
            GROUP BY e.experiment_id, e.name
        """)
        
        for experiment_name, model_count in cursor.fetchall():
            mlflow_models_total.labels(experiment_name=experiment_name).inc(model_count)
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error collecting metrics: {e}")

def main():
    """Main function"""
    print("Starting MLflow Exporter...")
    
    # Start Prometheus HTTP server
    start_http_server(8000)
    print("MLflow Exporter started on port 8000")
    
    # Collect metrics every 30 seconds
    while True:
        collect_metrics()
        time.sleep(30)

if __name__ == "__main__":
    main() 