import os
import mlflow
import mlflow.sklearn
import mlflow.xgboost
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import warnings
warnings.simplefilter("ignore")

from config import (
    MLFLOW_TRACKING_URI,
    MLFLOW_EXPERIMENT_NAME,
    MLFLOW_S3_ENDPOINT_URL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB
)

# Setup
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

models = {
    "LinearRegression": os.path.join(BASE_DIR, "models", "LinearRegression.sav"),
    "RandomForestRegressor": os.path.join(BASE_DIR, "models", "RandomForestRegressor.sav"),
    "XGBoostRegressor": os.path.join(BASE_DIR, "models", "XGBoostRegressor.sav")
}

def load_and_preprocess_data():
    try:
        data_path = os.path.join(BASE_DIR, "CarPrice_Assignment.csv")
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Dataset not found at {data_path}")
        data = pd.read_csv(data_path)
        print("✅ Dataset loaded")

        # Ambil brand
        data['carbrand'] = data['CarName'].apply(lambda x: x.split(' ')[0].lower())

        # Bersihkan typo brand
        data['carbrand'] = data['carbrand'].replace({
            'toyouta': 'toyota',
            'porcshce': 'porsche',
            'vokswagen': 'volkswagen',
            'vw': 'volkswagen',
            'maxda': 'mazda'
        })

        # One-hot encoding
        categorical_cols = ['fueltype', 'aspiration', 'doornumber', 'carbody', 
                            'drivewheel', 'enginelocation', 'enginetype', 
                            'cylindernumber', 'fuelsystem', 'carbrand']

        data_encoded = pd.get_dummies(data, columns=categorical_cols, drop_first=True)
        print("✅ One-hot encoding done")

        return data_encoded
    except Exception as e:
        print(f"❌ Error preprocessing data: {str(e)}")
        return None

def get_model_parameters(model_name, model):
    base_params = {
        "test_size": 0.2,
        "random_state": 42,
        "scaling": "StandardScaler",
        "model_type": model_name
    }
    try:
        if model_name == "LinearRegression":
            base_params.update({
                "fit_intercept": str(model.fit_intercept),
                "normalize": "False"
            })
        elif model_name == "RandomForestRegressor":
            base_params.update({
                "n_estimators": getattr(model, "n_estimators", 100),
                "max_depth": str(getattr(model, "max_depth", None)),
                "min_samples_split": getattr(model, "min_samples_split", 2),
                "min_samples_leaf": getattr(model, "min_samples_leaf", 1),
                "max_features": str(getattr(model, "max_features", "auto")),
                "bootstrap": getattr(model, "bootstrap", True)
            })
        elif model_name == "XGBoostRegressor":
            base_params.update({
                "n_estimators": getattr(model, "n_estimators", 100),
                "max_depth": getattr(model, "max_depth", 6),
                "learning_rate": getattr(model, "learning_rate", 0.1),
                "subsample": getattr(model, "subsample", 0.8),
                "colsample_bytree": getattr(model, "colsample_bytree", 0.8),
                "gamma": getattr(model, "gamma", 0),
                "reg_alpha": getattr(model, "reg_alpha", 0),
                "reg_lambda": getattr(model, "reg_lambda", 1)
            })
        return base_params
    except Exception as e:
        print(f"❌ Error getting parameters for {model_name}: {str(e)}")
        return base_params

def log_model(model_name, model_path):
    try:
        print(f"\n🎯 Processing {model_name}...")

        # Load dan preprocessing data
        data_encoded = load_and_preprocess_data()
        if data_encoded is None:
            print(f"❌ Data gagal diproses")
            return

        X = data_encoded.drop(['price', 'CarName'], axis=1)
        y = data_encoded['price']

        # Simpan fitur kolom
        feature_file = os.path.join(BASE_DIR, "models", f"{model_name}_features.pkl")
        feature_columns = X.columns.tolist()
        joblib.dump(feature_columns, feature_file)
        print(f"📄 Saved feature columns to {feature_file}")

        # Reindex hanya untuk memastikan konsistensi jika di-run berulang
        X = X.reindex(columns=feature_columns, fill_value=0)

        # Split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale numerik
        numeric_cols = ['wheelbase', 'carheight', 'horsepower', 'peakrpm', 'citympg']
        existing = [col for col in numeric_cols if col in X_train.columns]
        if existing:
            scaler = StandardScaler()
            X_train[existing] = scaler.fit_transform(X_train[existing])
            X_test[existing] = scaler.transform(X_test[existing])
            print("📊 Feature scaling applied")

            # Simpan scaler ke file .pkl
            scaler_path = os.path.join(BASE_DIR, "models", f"{model_name}_scaler.pkl")
            joblib.dump(scaler, scaler_path)
            print(f"💾 Saved scaler to {scaler_path}")
    
        # 🔁 Train model dari awal
        if model_name == "LinearRegression":
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
        elif model_name == "RandomForestRegressor":
            from sklearn.ensemble import RandomForestRegressor
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        elif model_name == "XGBoostRegressor":
            from xgboost import XGBRegressor
            model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42)

        model.fit(X_train, y_train)
        joblib.dump(model, model_path)
        print(f"💾 Re-trained and saved model to {model_path}")

        # Prediksi dan evaluasi
        y_pred = model.predict(X_test)

        metrics = {
            'r2_score': r2_score(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred),
            'mape': mean_absolute_percentage_error(y_test, y_pred) * 100
        }

        params = get_model_parameters(model_name, model)

        # Log ke MLflow
        with mlflow.start_run(run_name=f"{model_name}_freshly_trained"):
            mlflow.log_params(params)
            mlflow.log_metrics(metrics)

            if model_name == "XGBoostRegressor":
                mlflow.xgboost.log_model(model, artifact_path="models", registered_model_name=model_name)
            else:
                mlflow.sklearn.log_model(model, artifact_path="models", registered_model_name=model_name)

            print(f"✅ Logged {model_name} to MLflow")
            print(f"📊 Metrics: {metrics}")
            print(f"🔧 Params: {params}")

    except Exception as e:
        print(f"❌ Error logging {model_name}: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting MLflow Logging")
    print(f"MLflow URI: {MLFLOW_TRACKING_URI}")
    print(f"Experiment: {MLFLOW_EXPERIMENT_NAME}")
    print("=" * 60)

    for model_name, model_path in models.items():
        log_model(model_name, model_path)

    print("\n🎉 Done! Check MLflow UI.")
