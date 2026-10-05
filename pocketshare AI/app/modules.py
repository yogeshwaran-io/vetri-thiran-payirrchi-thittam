from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    email: Mapped[str] = Column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = Column(String(80), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = Column(String(255), nullable=False)
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)

    histories: Mapped[list["PlannerHistory"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class PlannerHistory(Base):
    __tablename__ = "planner_history"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    destination: Mapped[str] = Column(String(255), nullable=False)
    title: Mapped[str] = Column(String(255), nullable=False)
    summary: Mapped[str] = Column(Text, nullable=False)
    payload: Mapped[dict] = Column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="histories")
