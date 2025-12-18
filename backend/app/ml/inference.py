import os
import joblib
import logging

logger = logging.getLogger(__name__)

MODEL_PATH = os.getenv(
    "MODEL_PATH",
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "artifacts", "airvalue_model.joblib")
    )
)

class PriceModel:
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            logger.error("Model artifact missing at %s", MODEL_PATH)
            raise RuntimeError("Model artifact missing")

        self.model = joblib.load(MODEL_PATH)
        logger.info("ML model loaded from %s", MODEL_PATH)

    def predict(self, features: dict) -> float:
        X = [[
            features["bedrooms"],
            features["bathrooms"],
            features["location_score"],
            features["amenities_score"]
        ]]
        price = float(self.model.predict(X)[0])
        logger.info("Prediction generated: %.2f", price)
        return price
