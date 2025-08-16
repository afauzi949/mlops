export interface CarData {
  car_ID: number;
  CarName: string;
  fueltype: string;
  aspiration: string;
  doornumber: string;
  carbody: string;
  drivewheel: string;
  enginelocation: string;
  wheelbase: number;
  carheight: number;
  enginetype: string;
  cylindernumber: string;
  fuelsystem: string;
  horsepower: number;
  peakrpm: number;
  citympg: number;
}

export interface PredictionResponse {
  predictions: Array<{
    predicted_price: number;
  }>;
}

export interface CarFormData {
  CarName: string;
  fueltype: string;
  aspiration: string;
  doornumber: string;
  carbody: string;
  drivewheel: string;
  enginelocation: string;
  wheelbase: number;
  carheight: number;
  enginetype: string;
  cylindernumber: string;
  fuelsystem: string;
  horsepower: number;
  peakrpm: number;
  citympg: number;
}
