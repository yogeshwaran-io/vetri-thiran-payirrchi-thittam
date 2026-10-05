from __future__ import annotations


def build_recommendations(
    destination: str,
    interests: list[str] | None,
    budget: float,
    travelers: int,
) -> list[str]:
    items = [
        f"Book a central stay in {destination} to save on transit",
        "Prioritize one signature experience and keep the rest flexible",
        "Use local food markets for authentic meals within budget",
    ]
    if interests:
        items.insert(0, f"Match activities around: {', '.join(interests[:3])}")
    if budget < 250:
        items.append("Choose low-cost public transport and free walking tours")
    if travelers > 2:
        items.append("Consider grouped tickets or apartment stays for better value")
    return items
