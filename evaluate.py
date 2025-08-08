import os
import pandas as pd
import numpy as np
import joblib
from preprocess import preprocess_data
from model import load_models, load_feature_cols
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

MODEL_DIR = "models"
TARGET_VARS = ["powerDemand", "price", "carbonIntensity"]
EVAL_HOURS = 24

def evaluate_models():
    print("Loading data...")
    df_raw = preprocess_data()
    df_numeric = df_raw.select_dtypes(include=np.number).copy()
    df_numeric["timestamp"] = df_raw["timestamp"]

    print("Loading models and feature columns...")
    models = load_models(TARGET_VARS)
    feature_cols_per_model = load_feature_cols()

    results = {}

    for target in TARGET_VARS:
        print(f"Evaluating model: {target}")
        if target not in models:
            print(f"Model for {target} not found. Skipping.")
            continue

        feature_cols = feature_cols_per_model.get(target, [])
        if not feature_cols:
            print(f"No feature columns found for {target}. Skipping.")
            continue

        X = df_numeric[feature_cols]
        y = df_numeric[target]

        X_test = X.iloc[-EVAL_HOURS:]
        y_test = y.iloc[-EVAL_HOURS:]

        model = models[target]
        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        print(f"{target} -> MAE: {mae:.4f}, RMSE: {rmse:.4f}, R2: {r2:.4f}")

        results[target] = {
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2
        }

    return results

if __name__ == "__main__":
    metrics = evaluate_models()
