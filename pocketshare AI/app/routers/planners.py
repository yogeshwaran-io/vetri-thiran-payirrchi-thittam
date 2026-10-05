from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user_optional
from app.modules import PlannerHistory, User
from app.schemas import PlannerRequest, PlannerResponse
from app.routers.services.catalog_service import get_catalog_matches
from app.routers.services.recommendation_service import build_recommendations

router = APIRouter(prefix="", tags=["planner"])


@router.get("/planner")
def planner_page() -> dict[str, str]:
    return {"message": "Planner ready"}


@router.post("/planner", response_model=PlannerResponse)
@router.post("/planner/plan", response_model=PlannerResponse)
def create_plan(
    payload: PlannerRequest,
    db: Session = Depends(get_db),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> PlannerResponse:
    catalog = get_catalog_matches(payload.destination, payload.interests)
    recommendations = build_recommendations(
        payload.destination,
        payload.interests,
        payload.budget,
        payload.travelers,
    )

    itinerary = [
        f"Day 1: Explore {payload.destination} highlights and local culture",
        f"Day 2: Visit curated experiences aligned with {', '.join(payload.interests) if payload.interests else 'local highlights'}",
        f"Day 3: Enjoy food, shopping, and a flexible budget-friendly wrap-up",
    ]

    response = PlannerResponse(
        destination=payload.destination,
        title=f"{payload.destination} plan",
        summary=(
            f"A {payload.days}-day trip for {payload.travelers} traveler(s) "
            f"with a budget of ${payload.budget:,.0f}, focused on {', '.join(payload.interests) if payload.interests else 'local experiences'}"
        ),
        itinerary=itinerary[:payload.days],
        recommendations=recommendations,
        estimated_cost=min(payload.budget, max(payload.budget * 0.9, 1.0)),
        generated_at=datetime.now(UTC),
    )

    current_user = get_current_user_optional(authorization, db)
    if current_user is not None:
        history_item = PlannerHistory(
            user_id=current_user.id,
            destination=payload.destination,
            title=response.title,
            summary=response.summary,
            payload=response.model_dump(mode="json"),
        )
        db.add(history_item)
        db.commit()

    return response
