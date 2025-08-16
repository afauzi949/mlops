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

def setup_enhanced_dashboard():
    """Setup Enhanced Car Price Predictor Dashboard"""
    print("Setting up Enhanced Car Price Predictor Dashboard...")
    
    # Enhanced dashboard configuration - sama seperti yang ada + tambahan metrik
    dashboard_config = {
        "dashboard": {
            "title": "anjay",
            "tags": ["mlflow", "car-price", "ml-monitoring"],
            "style": "dark",
            "timezone": "browser",
            "panels": [
                {
                    "id": 1,
                    "title": "API Health Status",
                    "type": "stat",
                    "targets": [
                        {
                            "expr": "up{job=\"fastapi-app\"}",
                            "legendFormat": "FastAPI Backend"
                        },
                        {
                            "expr": "up{job=\"car-price-predictor\"}",
                            "legendFormat": "Frontend Container"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "color": {
                                "mode": "thresholds"
                            },
                            "thresholds": {
                                "steps": [
                                    {"color": "red", "value": 0},
                                    {"color": "green", "value": 1}
                                ]
                            },
                            "mappings": [
                                {
                                    "options": {
                                        "0": {"text": "DOWN", "color": "red"},
                                        "1": {"text": "UP", "color": "green"}
                                    },
                                    "type": "value"
                                }
                            ]
                        }
                    },
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
                },
                {
                    "id": 2,
                    "title": "Prediction Request Rate",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "rate(http_requests_total{job=\"fastapi-app\", handler=\"/predict\"}[5m])",
                            "legendFormat": "Predictions/sec"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "color": {
                                "mode": "palette-classic"
                            },
                            "custom": {
                                "axisLabel": "",
                                "axisPlacement": "auto",
                                "barAlignment": 0,
                                "drawStyle": "line",
                                "fillOpacity": 10,
                                "gradientMode": "none",
                                "hideFrom": {
                                    "legend": False,
                                    "tooltip": False,
                                    "vis": False
                                },
                                "lineInterpolation": "linear",
                                "lineWidth": 1,
                                "pointSize": 5,
                                "scaleDistribution": {
                                    "type": "linear"
                                },
                                "showPoints": "never",
                                "spanNulls": False,
                                "stacking": {
                                    "group": "A",
                                    "mode": "none"
                                },
                                "thresholdsStyle": {
                                    "mode": "off"
                                }
                            },
                            "mappings": [],
                            "thresholds": {
                                "mode": "absolute",
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "red", "value": 80}
                                ]
                            },
                            "unit": "reqps"
                        }
                    },
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
                },
                {
                    "id": 3,
                    "title": "Prediction Response Time",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job=\"fastapi-app\", handler=\"/predict\"}[5m]))",
                            "legendFormat": "95th percentile"
                        },
                        {
                            "expr": "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket{job=\"fastapi-app\", handler=\"/predict\"}[5m]))",
                            "legendFormat": "50th percentile"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "color": {
                                "mode": "palette-classic"
                            },
                            "custom": {
                                "axisLabel": "",
                                "axisPlacement": "auto",
                                "barAlignment": 0,
                                "drawStyle": "line",
                                "fillOpacity": 10,
                                "gradientMode": "none",
                                "hideFrom": {
                                    "legend": False,
                                    "tooltip": False,
                                    "vis": False
                                },
                                "lineInterpolation": "linear",
                                "lineWidth": 1,
                                "pointSize": 5,
                                "scaleDistribution": {
                                    "type": "linear"
                                },
                                "showPoints": "never",
                                "spanNulls": False,
                                "stacking": {
                                    "group": "A",
                                    "mode": "none"
                                },
                                "thresholdsStyle": {
                                    "mode": "off"
                                }
                            },
                            "mappings": [],
                            "thresholds": {
                                "mode": "absolute",
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "yellow", "value": 1},
                                    {"color": "red", "value": 5}
                                ]
                            },
                            "unit": "s"
                        }
                    },
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8}
                },
                {
                    "id": 4,
                    "title": "HTTP Status Codes",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "rate(http_requests_total{job=\"fastapi-app\", handler=\"/predict\", status=~\"2..\"}[5m])",
                            "legendFormat": "2xx Success"
                        },
                        {
                            "expr": "rate(http_requests_total{job=\"fastapi-app\", handler=\"/predict\", status=~\"4..\"}[5m])",
                            "legendFormat": "4xx Client Error"
                        },
                        {
                            "expr": "rate(http_requests_total{job=\"fastapi-app\", handler=\"/predict\", status=~\"5..\"}[5m])",
                            "legendFormat": "5xx Server Error"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "color": {
                                "mode": "palette-classic"
                            },
                            "custom": {
                                "axisLabel": "",
                                "axisPlacement": "auto",
                                "barAlignment": 0,
                                "drawStyle": "line",
                                "fillOpacity": 10,
                                "gradientMode": "none",
                                "hideFrom": {
                                    "legend": False,
                                    "tooltip": False,
                                    "vis": False
                                },
                                "lineInterpolation": "linear",
                                "lineWidth": 1,
                                "pointSize": 5,
                                "scaleDistribution": {
                                    "type": "linear"
                                },
                                "showPoints": "never",
                                "spanNulls": False,
                                "stacking": {
                                    "group": "A",
                                    "mode": "none"
                                },
                                "thresholdsStyle": {
                                    "mode": "off"
                                }
                            },
                            "mappings": [],
                            "thresholds": {
                                "mode": "absolute",
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "red", "value": 80}
                                ]
                            },
                            "unit": "reqps"
                        }
                    },
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8}
                },
                {
                    "id": 5,
                    "title": "Container CPU Usage",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "rate(container_cpu_usage_seconds_total{name=~\".*car-price.*\"}[5m]) * 100",
                            "legendFormat": "Frontend CPU %"
                        },
                        {
                            "expr": "rate(container_cpu_usage_seconds_total{name=~\".*fastapi.*\"}[5m]) * 100",
                            "legendFormat": "Backend CPU %"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "color": {
                                "mode": "palette-classic"
                            },
                            "custom": {
                                "axisLabel": "",
                                "axisPlacement": "auto",
                                "barAlignment": 0,
                                "drawStyle": "line",
                                "fillOpacity": 10,
                                "gradientMode": "none",
                                "hideFrom": {
                                    "legend": False,
                                    "tooltip": False,
                                    "vis": False
                                },
                                "lineInterpolation": "linear",
                                "lineWidth": 1,
                                "pointSize": 5,
                                "scaleDistribution": {
                                    "type": "linear"
                                },
                                "showPoints": "never",
                                "spanNulls": False,
                                "stacking": {
                                    "group": "A",
                                    "mode": "normal"
                                },
                                "thresholdsStyle": {
                                    "mode": "off"
                                }
                            },
                            "mappings": [],
                            "thresholds": {
                                "mode": "absolute",
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "yellow", "value": 70},
                                    {"color": "red", "value": 90}
                                ]
                            },
                            "unit": "percent"
                        }
                    },
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 16}
                },
                {
                    "id": 6,
                    "title": "Container Memory Usage",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "container_memory_usage_bytes{name=~\".*car-price.*\"} / 1024 / 1024",
                            "legendFormat": "Frontend Memory (MB)"
                        },
                        {
                            "expr": "container_memory_usage_bytes{name=~\".*fastapi.*\"} / 1024 / 1024",
                            "legendFormat": "Backend Memory (MB)"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "color": {
                                "mode": "palette-classic"
                            },
                            "custom": {
                                "axisLabel": "",
                                "axisPlacement": "auto",
                                "barAlignment": 0,
                                "drawStyle": "line",
                                "fillOpacity": 10,
                                "gradientMode": "none",
                                "hideFrom": {
                                    "legend": False,
                                    "tooltip": False,
                                    "vis": False
                                },
                                "lineInterpolation": "linear",
                                "lineWidth": 1,
                                "pointSize": 5,
                                "scaleDistribution": {
                                    "type": "linear"
                                },
                                "showPoints": "never",
                                "spanNulls": False,
                                "stacking": {
                                    "group": "A",
                                    "mode": "normal"
                                },
                                "thresholdsStyle": {
                                    "mode": "off"
                                }
                            },
                            "mappings": [],
                            "thresholds": {
                                "mode": "absolute",
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "yellow", "value": 80},
                                    {"color": "red", "value": 95}
                                ]
                            },
                            "unit": "bytes"
                        }
                    },
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 16}
                },
                {
                    "id": 7,
                    "title": "Total Predictions Made",
                    "type": "stat",
                    "targets": [
                        {
                            "expr": "increase(http_requests_total{job=\"fastapi-app\", handler=\"/predict\", status=~\"2..\"}[24h])",
                            "legendFormat": "Last 24h"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "color": {
                                "mode": "palette-classic"
                            },
                            "custom": {
                                "displayMode": "auto"
                            },
                            "mappings": [],
                            "thresholds": {
                                "mode": "absolute",
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "red", "value": 80}
                                ]
                            },
                            "unit": "short"
                        }
                    },
                    "gridPos": {"h": 8, "w": 12, "x": 0, "y": 24}
                },
                {
                    "id": 8,
                    "title": "Error Rate",
                    "type": "stat",
                    "targets": [
                        {
                            "expr": "rate(http_requests_total{job=\"fastapi-app\", handler=\"/predict\", status=~\"5..\"}[5m]) / rate(http_requests_total{job=\"fastapi-app\", handler=\"/predict\"}[5m]) * 100",
                            "legendFormat": "Error Rate %"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "color": {
                                "mode": "palette-classic"
                            },
                            "custom": {
                                "displayMode": "auto"
                            },
                            "mappings": [],
                            "thresholds": {
                                "mode": "absolute",
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "yellow", "value": 5},
                                    {"color": "red", "value": 10}
                                ]
                            },
                            "unit": "percent"
                        }
                    },
                    "gridPos": {"h": 8, "w": 12, "x": 12, "y": 24}
                },
                {
                    "id": 9,
                    "title": "Model R² Score",
                    "type": "stat",
                    "targets": [
                        {
                            "expr": "ml_model_r2",
                            "legendFormat": "R²"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "color": {
                                "mode": "palette-classic"
                            },
                            "custom": {
                                "displayMode": "auto"
                            },
                            "mappings": [],
                            "thresholds": {
                                "mode": "absolute",
                                "steps": [
                                    {"color": "red", "value": None},
                                    {"color": "yellow", "value": 0.5},
                                    {"color": "green", "value": 0.7}
                                ]
                            },
                            "unit": "short"
                        }
                    },
                    "gridPos": {"h": 8, "w": 8, "x": 0, "y": 32}
                },
                {
                    "id": 10,
                    "title": "VPS CPU Usage",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
                            "legendFormat": "CPU Usage %"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "color": {
                                "mode": "palette-classic"
                            },
                            "custom": {
                                "axisLabel": "",
                                "axisPlacement": "auto",
                                "barAlignment": 0,
                                "drawStyle": "line",
                                "fillOpacity": 10,
                                "gradientMode": "none",
                                "hideFrom": {
                                    "legend": False,
                                    "tooltip": False,
                                    "vis": False
                                },
                                "lineInterpolation": "linear",
                                "lineWidth": 1,
                                "pointSize": 5,
                                "scaleDistribution": {
                                    "type": "linear"
                                },
                                "showPoints": "never",
                                "spanNulls": False,
                                "stacking": {
                                    "group": "A",
                                    "mode": "none"
                                },
                                "thresholdsStyle": {
                                    "mode": "off"
                                }
                            },
                            "mappings": [],
                            "thresholds": {
                                "mode": "absolute",
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "yellow", "value": 70},
                                    {"color": "red", "value": 90}
                                ]
                            },
                            "unit": "percent"
                        }
                    },
                    "gridPos": {"h": 8, "w": 8, "x": 8, "y": 32}
                },
                {
                    "id": 11,
                    "title": "VPS Memory Usage",
                    "type": "timeseries",
                    "targets": [
                        {
                            "expr": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100",
                            "legendFormat": "Memory Usage %"
                        }
                    ],
                    "fieldConfig": {
                        "defaults": {
                            "color": {
                                "mode": "palette-classic"
                            },
                            "custom": {
                                "axisLabel": "",
                                "axisPlacement": "auto",
                                "barAlignment": 0,
                                "drawStyle": "line",
                                "fillOpacity": 10,
                                "gradientMode": "none",
                                "hideFrom": {
                                    "legend": False,
                                    "tooltip": False,
                                    "vis": False
                                },
                                "lineInterpolation": "linear",
                                "lineWidth": 1,
                                "pointSize": 5,
                                "scaleDistribution": {
                                    "type": "linear"
                                },
                                "showPoints": "never",
                                "spanNulls": False,
                                "stacking": {
                                    "group": "A",
                                    "mode": "none"
                                },
                                "thresholdsStyle": {
                                    "mode": "off"
                                }
                            },
                            "mappings": [],
                            "thresholds": {
                                "mode": "absolute",
                                "steps": [
                                    {"color": "green", "value": None},
                                    {"color": "yellow", "value": 80},
                                    {"color": "red", "value": 95}
                                ]
                            },
                            "unit": "percent"
                        }
                    },
                    "gridPos": {"h": 8, "w": 8, "x": 16, "y": 32}
                }
            ],
            "time": {
                "from": "now-1h",
                "to": "now"
            },
            "timepicker": {},
            "templating": {
                "list": []
            },
            "annotations": {
                "list": []
            },
            "refresh": "30s",
            "schemaVersion": 27,
            "version": 1,
            "links": []
        }
    }
    
    headers = get_auth_headers()
    
    try:
        response = requests.post(
            f"{GRAFANA_URL}/api/dashboards/db",
            headers=headers,
            json={"dashboard": dashboard_config["dashboard"], "overwrite": True}
        )
        
        if response.status_code == 200:
            print("Enhanced Car Price Predictor Dashboard configured successfully!")
            return True
        else:
            print(f"Failed to setup dashboard: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error setting up dashboard: {e}")
        return False

def main():
    print("Setting up Enhanced Car Price Predictor Dashboard...")
    
    if not wait_for_grafana():
        print("Grafana is not ready. Exiting.")
        sys.exit(1)
    
    if not setup_datasource():
        print("Failed to setup datasource. Exiting.")
        sys.exit(1)
    
    if not setup_enhanced_dashboard():
        print("Failed to setup dashboard. Exiting.")
        sys.exit(1)
    
    print("\n�� Enhanced Car Price Predictor Dashboard setup completed successfully!")
    print(f"�� Access Grafana at: {GRAFANA_URL}")
    print(f"🔑 Login with: {GRAFANA_USER}:{GRAFANA_PASSWORD}")
    print("�� Enhanced Dashboard should be available automatically")
    print("\n�� Dashboard includes:")
    print("   • API Health Status")
    print("   • Prediction Request Rate")
    print("   • Prediction Response Time")
    print("   • HTTP Status Codes")
    print("   • Container CPU Usage")
    print("   • Container Memory Usage")
    print("   • Total Predictions Made")
    print("   • Error Rate")
    print("   • Model R² Score (NEW)")
    print("   • VPS CPU Usage (NEW)")
    print("   • VPS Memory Usage (NEW)")

if __name__ == "__main__":
    main()