import joblib
import os
import numpy as np
from typing import Dict, Any


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "airvalue_rf_model.joblib")

try:
    model = joblib.load(MODEL_PATH)
    FEATURE_ORDER = list(model.feature_names_in_)
except Exception as e:
    model = None
    FEATURE_ORDER = []
    print(f"[ML ERROR] Failed to load model: {e}")


def validate_and_prepare_features(features: Dict[str, Any]) -> np.ndarray:
    if model is None:
        raise RuntimeError("ML model not loaded")

    vector = []

    for feature in FEATURE_ORDER:
        if feature not in features:
            raise ValueError(f"Missing required feature: {feature}")

        try:
            vector.append(float(features[feature]))
        except ValueError:
            raise ValueError(f"Invalid value for feature '{feature}'")

    return np.array(vector).reshape(1, -1)


def predict_price(features: Dict[str, Any]) -> float:
    X = validate_and_prepare_features(features)
    prediction = model.predict(X)[0]
    return round(float(prediction), 2)
