from fastapi import APIRouter, Depends, HTTPException, status
from app.core.auth_dependency import get_current_user

router = APIRouter(prefix="/premium", tags=["premium"])


@router.post("/dynamic-pricing")
def dynamic_pricing(current_user=Depends(get_current_user)):
    if current_user["role"] != "premium":
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Premium Feature – Upgrade Required",
        )

    return {"message": "Dynamic pricing activated"}
