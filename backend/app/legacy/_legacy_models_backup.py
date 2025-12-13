from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, unique=True)
    password_hash: str
    is_premium: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Property(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str
    bedrooms: int
    bathrooms: int
    area: float
    zipcode: str
    has_wifi: bool = False
    has_ac: bool = False
    is_entire_place: bool = True
    predicted_price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Premium placeholder tables
class Subscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    status: str = "trial"
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ends_at: Optional[datetime] = None

class BulkJob(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    status: str = "queued"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    result_path: Optional[str] = None
