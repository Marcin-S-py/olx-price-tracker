from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str = Field(..., max_length=72)

    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class PriceHistory(BaseModel):
    id: int
    offer_id: int
    price: Optional[float]
    checked_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OfferCreate(BaseModel):
    url: str

    model_config = ConfigDict(from_attributes=True)

class Offer(BaseModel):
    id: int
    url: str
    title: Optional[str]
    current_price: Optional[float]
    user_id: int
    prices: list[PriceHistory] = []

    model_config = ConfigDict(from_attributes=True)