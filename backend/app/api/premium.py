from fastapi import APIRouter, Depends, HTTPException, status
from app.core.auth_dependency import get_current_user

router = APIRouter(prefix="/premium", tags=["premium"])

@router.post("/bulk-predict")
def bulk_predict_placeholder(
    current_user=Depends(get_current_user),
):
    raise HTTPException(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        detail="Premium Feature – Upgrade Required",
    )
