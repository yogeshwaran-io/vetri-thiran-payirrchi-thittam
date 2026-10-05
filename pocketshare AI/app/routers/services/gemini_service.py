from __future__ import annotations

from app.config import get_settings

settings = get_settings()


def generate_itinerary(
    destination: str,
    budget: float,
    days: int,
    interests: list[str] | None = None,
    travelers: int = 2,
) -> dict[str, object]:
    if not settings.gemini_api_key:
        return {
            "title": f"{destination} quick itinerary",
            "summary": f"A {days}-day trip to {destination} for {travelers} traveler(s) within a ${budget:,.0f} budget.",
            "itinerary": [
                f"Day 1: settle in and explore the neighborhood",
                f"Day 2: focus on {' , '.join(interests or ['local highlights'])}",
                "Day 3: finish with food, shopping, and a scenic route",
            ],
            "recommendations": [
                "Keep one unstructured block for spontaneous exploration",
                "Reserve the highest-cost item early",
            ],
        }

    return {
        "title": f"{destination} AI itinerary",
        "summary": f"AI-assisted plan for {travelers} traveler(s) to {destination} with a ${budget:,.0f} budget.",
        "itinerary": [
            "Morning arrival and neighborhood orientation",
            "Midday local experiences and lunch",
            "Evening free time and dinner",
        ],
        "recommendations": [
            "Check the weather before finalizing outdoor activities",
            "Build in buffer time between sightseeing stops",
        ],
    }
