from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime


class PredictionRequest(BaseModel):
    features: Dict[str, Any]


class PredictionResponse(BaseModel):
    predicted_price: float
    explanation: Optional[Dict[str, float]]


class PredictionHistoryResponse(BaseModel):
    id: int
    features: Dict[str, Any]
    predicted_price: float
    created_at: datetime

    class Config:
        orm_mode = True
