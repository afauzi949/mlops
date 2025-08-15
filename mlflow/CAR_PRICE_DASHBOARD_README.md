# Car Price Predictor ML Dashboard

## 📊 Overview

Dashboard Grafana khusus untuk monitoring performa sistem Car Price Predictor yang menampilkan metrics ML yang relevan dengan project ini.

## 🎯 Metrics yang Ditampilkan

### 1. **API Health Status**
- Status UP/DOWN untuk FastAPI Backend dan Frontend Container
- Monitoring kesehatan sistem secara real-time

### 2. **Prediction Request Rate**
- Jumlah request prediksi per detik
- Monitoring traffic prediksi secara real-time

### 3. **Prediction Response Time**
- Response time 50th dan 95th percentile
- Monitoring performa prediksi model

### 4. **HTTP Status Codes**
- Distribusi status code (2xx, 4xx, 5xx)
- Monitoring error rate dan success rate

### 5. **Container CPU Usage**
- CPU usage untuk Frontend dan Backend container
- Monitoring resource utilization

### 6. **Container Memory Usage**
- Memory usage untuk Frontend dan Backend container
- Monitoring memory consumption

### 7. **Total Predictions Made**
- Total prediksi yang berhasil dalam 24 jam terakhir
- Business metrics

### 8. **Error Rate**
- Persentase error rate dari total request
- Monitoring reliability sistem

## 🚀 Setup dan Deployment

### 1. **Build dan Deploy Metrics Exporter**

```bash
# Build car price metrics exporter
docker-compose up --build car-price-metrics-exporter -d

# Restart Prometheus untuk mengambil target baru
docker-compose restart prometheus
```

### 2. **Setup Dashboard di Grafana**

```bash
# Jalankan script setup dashboard
python3 setup-car-price-dashboard.py
```

### 3. **Akses Dashboard**

- **URL**: http://localhost:3000
- **Username**: admin
- **Password**: muntilan
- **Dashboard**: "Car Price Predictor ML Dashboard"

## 📈 Custom Metrics yang Ditambahkan

### **Car Price Prediction Metrics**
- `car_price_prediction_requests_total`: Total request prediksi
- `car_price_prediction_duration_seconds`: Durasi prediksi
- `car_price_prediction_price_range`: Distribusi harga prediksi
- `car_price_model_accuracy`: Akurasi model
- `car_price_model_last_updated_timestamp`: Timestamp update terakhir

### **Metrics Categories**
- **Low Price**: < $10,000
- **Medium Price**: $10,000 - $25,000  
- **High Price**: > $25,000

## 🔧 Konfigurasi

### **Prometheus Targets**
```yaml
# Car Price Prediction metrics via custom exporter
- job_name: 'car-price-metrics-exporter'
  static_configs:
    - targets: ['car-price-metrics-exporter:8003']
  metrics_path: '/metrics'
  scrape_interval: 30s
```

### **Docker Services**
```yaml
car-price-metrics-exporter:
  build:
    context: .
    dockerfile: Dockerfile.car-price-exporter
  ports:
    - "8003:8003"
  environment:
    - POSTGRES_HOST=postgres
    - POSTGRES_PORT=5432
    - POSTGRES_DB=${POSTGRES_DB}
    - POSTGRES_USER=${POSTGRES_USER}
    - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
  depends_on:
    - postgres
    - mlflow-fastapi-app
```

## 📋 Alerting Rules (Opsional)

Tambahkan alerting rules berikut ke `alert.rules.yml`:

```yaml
# High Error Rate Alert
- alert: HighCarPricePredictionErrorRate
  expr: rate(car_price_prediction_requests_total{status="error"}[5m]) / rate(car_price_prediction_requests_total[5m]) > 0.05
  for: 2m
  labels:
    severity: warning
  annotations:
    summary: "High error rate in car price predictions"
    description: "Error rate is {{ $value | humanizePercentage }}"

# High Response Time Alert
- alert: HighCarPricePredictionResponseTime
  expr: histogram_quantile(0.95, rate(car_price_prediction_duration_seconds_bucket[5m])) > 3
  for: 2m
  labels:
    severity: warning
  annotations:
    summary: "High response time in car price predictions"
    description: "95th percentile response time is {{ $value }}s"

# Model Accuracy Degradation Alert
- alert: CarPriceModelAccuracyDegradation
  expr: car_price_model_accuracy < 0.8
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Car price model accuracy is below threshold"
    description: "Model accuracy is {{ $value }}"
```

## 🎨 Dashboard Features

### **Real-time Monitoring**
- Auto-refresh setiap 30 detik
- Real-time metrics collection
- Live system health monitoring

### **Visualization Types**
- **Stat Panels**: Untuk metrics sederhana (health status, totals)
- **Graph Panels**: Untuk time-series data (rates, response times)
- **Histogram**: Untuk distribusi data (price ranges)

### **Color Coding**
- **Green**: Healthy/Normal
- **Yellow**: Warning threshold
- **Red**: Critical threshold

## 🔍 Troubleshooting

### **Dashboard Tidak Muncul**
1. Cek apakah script setup berhasil dijalankan
2. Verifikasi file dashboard JSON ada di lokasi yang benar
3. Cek log Grafana untuk error

### **Metrics Tidak Muncul**
1. Cek apakah car-price-metrics-exporter berjalan
2. Verifikasi Prometheus target status
3. Cek koneksi database dan API

### **High Error Rate**
1. Cek log FastAPI application
2. Verifikasi model file ada dan bisa di-load
3. Cek resource utilization (CPU/Memory)

## 📊 Business Insights

Dashboard ini memberikan insights untuk:

1. **Performance Monitoring**: Response time dan throughput
2. **Reliability Tracking**: Error rates dan uptime
3. **Resource Planning**: CPU dan memory usage trends
4. **Business Metrics**: Total predictions dan success rates
5. **Model Health**: Accuracy tracking dan model updates

## 🔄 Maintenance

### **Regular Tasks**
- Monitor dashboard performance
- Update alerting thresholds jika diperlukan
- Review dan optimize metrics collection
- Backup dashboard configuration

### **Scaling Considerations**
- Monitor Prometheus storage usage
- Consider metrics retention policies
- Plan for horizontal scaling jika diperlukan
