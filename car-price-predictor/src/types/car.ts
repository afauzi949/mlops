export interface CarData {
  car_ID: number;
  symboling: number;
  carbrand: string;
  cartype: string;
  fueltype: string;
  aspiration: string;
  doornumber: string;
  carbody: string;
  drivewheel: string;
  enginelocation: string;
  wheelbase: number;
  carlength: number;
  carwidth: number;
  carheight: number;
  curbweight: number;
  enginetype: string;
  cylindernumber: string;
  enginesize: number;
  fuelsystem: string;
  boreratio: number;
  stroke: number;
  compressionratio: number;
  horsepower: number;
  peakrpm: number;
  citympg: number;
  highwaympg: number;
}

export interface PredictionResponse {
  predictions: Array<{
    predicted_price: number;
  }>;
}

export interface CarFormData {
  symboling: number;
  carbrand: string;
  cartype: string;
  fueltype: string;
  aspiration: string;
  doornumber: string;
  carbody: string;
  drivewheel: string;
  enginelocation: string;
  wheelbase: number;
  carlength: number;
  carwidth: number;
  carheight: number;
  curbweight: number;
  enginetype: string;
  cylindernumber: string;
  enginesize: number;
  fuelsystem: string;
  boreratio: number;
  stroke: number;
  compressionratio: number;
  horsepower: number;
  peakrpm: number;
  citympg: number;
  highwaympg: number;
}
