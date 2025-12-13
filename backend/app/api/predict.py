from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.prediction_service import create_prediction
from app.core.auth_dependency import get_current_user

router = APIRouter(prefix="/predict", tags=["prediction"])


@router.post("", response_model=PredictionResponse)
def predict(
    request: PredictionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    prediction = create_prediction(
        db=db,
        user_id=current_user["user_id"],
        features=request.features,
    )

    return {
        "predicted_price": prediction.predicted_price,
        "explanation": None,
    }
