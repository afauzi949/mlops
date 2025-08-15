#!/usr/bin/env python3
import requests
import json
import time
import sys
import base64

# Grafana configuration
GRAFANA_URL = "http://localhost:3000"
GRAFANA_USER = "admin"
GRAFANA_PASSWORD = "muntilan"

def wait_for_grafana():
    """Wait for Grafana to be ready"""
    print("Waiting for Grafana to be ready...")
    for i in range(30):
        try:
            response = requests.get(f"{GRAFANA_URL}/api/health", timeout=5)
            if response.status_code == 200:
                print("Grafana is ready!")
                return True
        except:
            pass
        time.sleep(2)
    return False

def get_auth_headers():
    """Get authentication headers"""
    auth_string = f"{GRAFANA_USER}:{GRAFANA_PASSWORD}"
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
    
    return {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_b64}"
    }

def setup_datasource():
    """Setup Prometheus datasource"""
    print("Setting up Prometheus datasource...")
    
    datasource_config = {
        "name": "Prometheus",
        "type": "prometheus",
        "access": "proxy",
        "url": "http://prometheus:9090",
        "isDefault": True,
        "editable": True
    }
    
    headers = get_auth_headers()
    
    try:
        response = requests.post(
            f"{GRAFANA_URL}/api/datasources",
            headers=headers,
            json=datasource_config
        )
        
        if response.status_code in [200, 409]:  # 409 means already exists
            print("Prometheus datasource configured successfully!")
            return True
        else:
            print(f"Failed to setup datasource: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error setting up datasource: {e}")
        return False

def setup_dashboard():
    """Setup MLflow dashboard"""
    print("Setting up MLflow dashboard...")
    
    # Read dashboard JSON
    try:
        with open("grafana/dashboards/mlflow-overview.json", "r") as f:
            dashboard_config = json.load(f)
    except Exception as e:
        print(f"Error reading dashboard file: {e}")
        return False
    
    headers = get_auth_headers()
    
    try:
        response = requests.post(
            f"{GRAFANA_URL}/api/dashboards/db",
            headers=headers,
            json={"dashboard": dashboard_config["dashboard"], "overwrite": True}
        )
        
        if response.status_code == 200:
            print("MLflow dashboard configured successfully!")
            return True
        else:
            print(f"Failed to setup dashboard: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error setting up dashboard: {e}")
        return False

def main():
    print("Setting up Grafana monitoring...")
    
    if not wait_for_grafana():
        print("Grafana is not ready. Exiting.")
        sys.exit(1)
    
    if not setup_datasource():
        print("Failed to setup datasource. Exiting.")
        sys.exit(1)
    
    if not setup_dashboard():
        print("Failed to setup dashboard. Exiting.")
        sys.exit(1)
    
    print("\n🎉 Grafana setup completed successfully!")
    print(f"📊 Access Grafana at: {GRAFANA_URL}")
    print(f"🔑 Login with: {GRAFANA_USER}:{GRAFANA_PASSWORD}")
    print("📈 MLflow dashboard should be available automatically")

if __name__ == "__main__":
    main() 