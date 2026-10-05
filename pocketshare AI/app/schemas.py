from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=40)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PlannerRequest(BaseModel):
    destination: str = Field(..., min_length=2)
    budget: float = Field(..., gt=0)
    days: int = Field(default=3, gt=0)
    interests: list[str] = Field(default_factory=list)
    travelers: int = Field(default=2, gt=0)


class PlannerResponse(BaseModel):
    destination: str
    title: str
    summary: str
    itinerary: list[str]
    recommendations: list[str]
    estimated_cost: float
    generated_at: datetime


class HistoryItem(BaseModel):
    id: int
    destination: str
    title: str
    summary: str
    created_at: datetime
