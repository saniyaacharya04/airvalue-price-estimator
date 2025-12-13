"""
NOTE:
This file is used for offline model training or data generation.
It is not part of the runtime inference pipeline.
"""

"""
Train and save the RandomForest model.
"""

import os
from .ml_model import generate_synthetic_dataset
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

# directory containing this file: backend/app/
HERE = os.path.dirname(__file__)

# Save model one folder above: backend/airvalue_rf_model.joblib
MODEL_PATH = os.path.abspath(os.path.join(HERE, "..", "airvalue_rf_model.joblib"))

# Save sample CSV inside dataset folder (root-level)
CSV_PATH = os.path.abspath(os.path.join(HERE, "..", "..", "dataset", "sample_properties.csv"))

def train_and_save(n=1200):
    print("Generating synthetic dataset...")
    df = generate_synthetic_dataset(csv_out_path=CSV_PATH, n=n)

    df["zipcode_feat"] = df["zipcode"].astype(str).str[-3:].astype(int)

    X = df[["bedrooms", "bathrooms", "area", "zipcode_feat", "has_wifi", "has_ac", "is_entire_place"]]
    y = df["price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training RandomForestRegressor...")
    model = RandomForestRegressor(n_estimators=150, random_state=42)
    model.fit(X_train, y_train)

    print("Saving model to:", MODEL_PATH)
    joblib.dump(model, MODEL_PATH)

    score = model.score(X_test, y_test)
    print(f"Training complete. Test R²: {score:.4f}")

    return MODEL_PATH


if __name__ == "__main__":
    train_and_save()
