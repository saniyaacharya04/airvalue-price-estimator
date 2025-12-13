from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.auth_dependency import get_current_user
from app.schemas.prediction import PredictionHistoryResponse
from app.services.history_service import get_user_predictions

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=list[PredictionHistoryResponse])
def history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_user_predictions(db, current_user["user_id"])
