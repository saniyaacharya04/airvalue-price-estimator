from sqlalchemy.orm import Session
from app.models.prediction import Prediction
from app.ml.model import predict_price


def create_prediction(
    db: Session,
    user_id: int,
    features: dict,
):
    price = predict_price(features)

    prediction = Prediction(
        user_id=user_id,
        features=features,
        predicted_price=price,
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction
