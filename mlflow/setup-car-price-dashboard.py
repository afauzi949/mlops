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

def setup_car_price_dashboard():
    """Setup Car Price Predictor ML Dashboard"""
    print("Setting up Car Price Predictor ML Dashboard...")
    
    # Read dashboard JSON
    try:
        with open("grafana/dashboards/car-price-predictor-ml.json", "r") as f:
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
            print("Car Price Predictor ML Dashboard configured successfully!")
            return True
        else:
            print(f"Failed to setup dashboard: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error setting up dashboard: {e}")
        return False

def main():
    print("Setting up Car Price Predictor ML Dashboard...")
    
    if not wait_for_grafana():
        print("Grafana is not ready. Exiting.")
        sys.exit(1)
    
    if not setup_car_price_dashboard():
        print("Failed to setup dashboard. Exiting.")
        sys.exit(1)
    
    print("\n🎉 Car Price Predictor ML Dashboard setup completed successfully!")
    print(f"📊 Access Grafana at: {GRAFANA_URL}")
    print(f"🔑 Login with: {GRAFANA_USER}:{GRAFANA_PASSWORD}")
    print("📈 Car Price Predictor ML Dashboard should be available automatically")
    print("\n📋 Dashboard includes:")
    print("   • API Health Status")
    print("   • Prediction Request Rate")
    print("   • Prediction Response Time")
    print("   • HTTP Status Codes")
    print("   • Container CPU & Memory Usage")
    print("   • Total Predictions Made")
    print("   • Error Rate")

if __name__ == "__main__":
    main()
