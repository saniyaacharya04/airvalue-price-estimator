from pydantic import BaseModel, EmailStr
from typing import Optional

class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PredictRequest(BaseModel):
    title: Optional[str]
    bedrooms: int
    bathrooms: int
    area: float
    zipcode: str
    has_wifi: bool = False
    has_ac: bool = False
    is_entire_place: bool = True

class PredictResponse(BaseModel):
    predicted_price: float
    currency: str = "USD"
    model: str = "random_forest_v1"

class PropertyOut(BaseModel):
    id: int
    title: Optional[str]
    bedrooms: int
    bathrooms: int
    area: float
    zipcode: str
    has_wifi: bool
    has_ac: bool
    is_entire_place: bool
    predicted_price: float
