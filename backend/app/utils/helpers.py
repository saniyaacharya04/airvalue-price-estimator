# backend/app/utils.py
import os
import joblib
from .ml_model import ModelWrapper

MODEL_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "airvalue_rf_model.joblib"))

def load_or_train():
    """
    Return a model object. If saved model exists and loads, return it.
    Otherwise train from scratch using ModelWrapper (which trains internally).
    """
    if os.path.exists(MODEL_FILE):
        try:
            model = joblib.load(MODEL_FILE)
            return model
        except Exception:
            # fallback to training via ModelWrapper
            print("Saved model failed to load; training in-memory model as fallback.")
    # fallback: train via ModelWrapper (this will persist a joblib at default path)
    from .ml_model import MODEL
    return MODEL.model
