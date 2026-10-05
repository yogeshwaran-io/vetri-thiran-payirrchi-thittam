from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.modules import PlannerHistory, User
from app.schemas import HistoryItem

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=list[HistoryItem])
@router.get("/user", response_model=list[HistoryItem])
def list_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[HistoryItem]:
    history_rows = (
        db.query(PlannerHistory)
        .filter(PlannerHistory.user_id == current_user.id)
        .order_by(PlannerHistory.created_at.desc())
        .all()
    )

    return [
        HistoryItem(
            id=row.id,
            destination=row.destination,
            title=row.title,
            summary=row.summary,
            created_at=row.created_at,
        )
        for row in history_rows
    ]
