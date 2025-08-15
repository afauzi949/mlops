# Quick Start Guide

Get the Car Price Predictor running in 5 minutes!

## 🚀 Quick Start (Local Development)

### 1. Prerequisites
- Node.js 18+ installed
- npm or yarn

### 2. Clone and Install
```bash
git clone <repository-url>
cd car-price-predictor
npm install
```

### 3. Start Development Server
```bash
npm run dev
```

### 4. Open Browser
Navigate to http://localhost:3000

That's it! 🎉

## 🐳 Quick Start (Docker)

### 1. Prerequisites
- Docker installed

### 2. Clone and Run
```bash
git clone <repository-url>
cd car-price-predictor
docker-compose up -d
```

### 3. Open Browser
Navigate to http://localhost:3000

## 📱 Using the Application

### Single Car Prediction
1. Fill in the car specifications form
2. Click "Predict Price"
3. View the predicted price

### Batch Prediction
1. Go to http://localhost:3000/batch
2. Upload a CSV file with car data
3. Download the results

## 📁 Sample Data

Use the included `sample-data.csv` file to test batch predictions:

```bash
# The file contains 5 sample cars with all required fields
cat sample-data.csv
```

## 🔧 API Testing

Test the API directly:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '[{"car_ID":1,"symboling":3,"CarName":"alfa-romero giulia","fueltype":"gas","aspiration":"std","doornumber":"two","carbody":"convertible","drivewheel":"rwd","enginelocation":"front","wheelbase":88.6,"carlength":168.8,"carwidth":64.1,"carheight":48.8,"curbweight":2548,"enginetype":"dohc","cylindernumber":"four","enginesize":130,"fuelsystem":"mpfi","boreratio":3.47,"stroke":2.68,"compressionratio":9.0,"horsepower":111,"peakrpm":5000,"citympg":21,"highwaympg":27}]' \
  http://103.47.224.217:8080/predict
```

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Find what's using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>
```

### Docker Issues
```bash
# Clean up Docker
docker system prune -a

# Rebuild
docker-compose up --build
```

### API Connection Issues
- Check if the API server is running at http://103.47.224.217:8080
- Verify network connectivity

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed information
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Explore the code structure in `src/` directory

## 🆘 Need Help?

- Check the browser console for errors
- Review the application logs
- Open an issue in the GitHub repository

---

**Happy Predicting! 🚗💰**
