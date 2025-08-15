# Car Price Predictor

A modern, responsive web application for predicting car prices using machine learning. Built with Next.js, TypeScript, and Tailwind CSS.

## Features

### 🚗 Single Car Prediction
- Comprehensive form with 25+ car specifications
- Real-time validation and error handling
- Instant price predictions
- Responsive design for all devices

### 📊 Batch Prediction
- CSV file upload support
- Bulk processing of multiple cars
- Download results as CSV
- Progress indicators and error handling

### 🎨 Modern UI/UX
- Beautiful, responsive design
- Dark mode support
- Smooth animations and transitions
- Mobile-first approach

### ⚡ Fast & Reliable
- Optimized API calls
- Error handling and retry mechanisms
- Loading states and feedback
- TypeScript for type safety

## Tech Stack

- **Frontend**: Next.js 15, React 19, TypeScript
- **Styling**: Tailwind CSS 4
- **UI Components**: Custom components with Radix UI primitives
- **Forms**: React Hook Form with Zod validation
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Deployment**: Ready for Vercel/Docker

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd car-price-predictor
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

### API Configuration

The application is configured to use the API at `http://103.47.224.217:8080`. You can modify the API endpoint in `src/lib/api.ts`:

```typescript
const API_BASE_URL = 'http://103.47.224.217:8080';
```

## Usage

### Single Car Prediction

1. Navigate to the home page
2. Fill in the car specifications form
3. Click "Predict Price" to get instant results
4. View the predicted price in the results section

### Batch Prediction

1. Navigate to the batch prediction page
2. Prepare a CSV file with car specifications
3. Upload the CSV file
4. Wait for processing to complete
5. Download the results as a CSV file

### CSV Format Requirements

The CSV file should include the following columns:

```csv
car_ID,symboling,CarName,fueltype,aspiration,doornumber,carbody,drivewheel,enginelocation,wheelbase,carlength,carwidth,carheight,curbweight,enginetype,cylindernumber,enginesize,fuelsystem,boreratio,stroke,compressionratio,horsepower,peakrpm,citympg,highwaympg
1,3,"alfa-romero giulia",gas,std,two,convertible,rwd,front,88.6,168.8,64.1,48.8,2548,dohc,four,130,mpfi,3.47,2.68,9.0,111,5000,21,27
```

## API Endpoints

### POST /predict

Predicts car prices for one or more vehicles.

**Request Body:**
```json
[
  {
    "car_ID": 1,
    "symboling": 3,
    "CarName": "alfa-romero giulia",
    "fueltype": "gas",
    "aspiration": "std",
    "doornumber": "two",
    "carbody": "convertible",
    "drivewheel": "rwd",
    "enginelocation": "front",
    "wheelbase": 88.6,
    "carlength": 168.8,
    "carwidth": 64.1,
    "carheight": 48.8,
    "curbweight": 2548,
    "enginetype": "dohc",
    "cylindernumber": "four",
    "enginesize": 130,
    "fuelsystem": "mpfi",
    "boreratio": 3.47,
    "stroke": 2.68,
    "compressionratio": 9.0,
    "horsepower": 111,
    "peakrpm": 5000,
    "citympg": 21,
    "highwaympg": 27
  }
]
```

**Response:**
```json
{
  "predictions": [
    {
      "predicted_price": 9744.857421875
    }
  ]
}
```

## Project Structure

```
src/
├── app/                    # Next.js app directory
│   ├── batch/             # Batch prediction page
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # Reusable UI components
│   ├── batch-prediction.tsx
│   └── car-prediction-form.tsx
├── lib/                  # Utility functions
│   ├── api.ts           # API functions
│   └── utils.ts         # Helper functions
└── types/               # TypeScript type definitions
    └── car.ts
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Deploy automatically

### Docker

1. Build the Docker image:
```bash
docker build -t car-price-predictor .
```

2. Run the container:
```bash
docker run -p 3000:3000 car-price-predictor
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue in the GitHub repository or contact the development team.
