from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import os

router = APIRouter()

# ==== Input Schema ====
class CarFeatures(BaseModel):
    carname: str
    wheelbase: float
    carheight: float
    horsepower: float
    peakrpm: float
    citympg: float
    fueltype: str
    aspiration: str
    doornumber: str
    carbody: str
    drivewheel: str
    enginelocation: str
    enginetype: str
    cylindernumber: str
    fuelsystem: str

# ==== Load model, features & scaler ====
base_path = os.path.join(os.path.dirname(__file__), "../../models")

model = joblib.load(os.path.join(base_path, "XGBoostRegressor.sav"))
expected_features = joblib.load(os.path.join(base_path, "XGBoostRegressor_features.pkl"))
scaler = joblib.load(os.path.join(base_path, "XGBoostRegressor_scaler.pkl"))

numerical_cols = ['wheelbase', 'carheight', 'horsepower', 'peakrpm', 'citympg']

@router.post("/predict")
def predict_price(features: CarFeatures):
    # Extract brand
    carbrand = features.carname.split(" ")[0].lower()

    # Convert input to dict
    input_dict = features.dict()
    input_dict['carbrand'] = carbrand
    del input_dict['carname']

    # Convert to DataFrame
    df = pd.DataFrame([input_dict])

    # One-hot encode categorical columns
    categorical_cols = ['fueltype', 'aspiration', 'doornumber', 'carbody', 
                        'drivewheel', 'enginelocation', 'enginetype', 
                        'cylindernumber', 'fuelsystem', 'carbrand']
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Terapkan scaling hanya ke kolom yang tersedia
    existing_cols = [col for col in numerical_cols if col in df_encoded.columns]
    if existing_cols:
        df_encoded[existing_cols] = scaler.transform(df_encoded[existing_cols])

    # Reindex to match model input
    df_encoded = df_encoded.reindex(columns=expected_features, fill_value=0)

    # Predict
    prediction = model.predict(df_encoded)[0]

    return {"predicted_price": round(float(prediction), 2)}
