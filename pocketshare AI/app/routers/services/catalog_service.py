from __future__ import annotations


def get_catalog_matches(destination: str, interests: list[str] | None = None) -> list[str]:
    normalized = destination.strip()
    base = [
        "local dining",
        "guided experiences",
        "nightlife",
        "historic tours",
        "outdoor activities",
    ]
    if not normalized:
        return base

    interest_list = [item.strip().lower() for item in (interests or []) if item.strip()]
    if not interest_list:
        return [f"{normalized} highlights", *base]

    return [f"{normalized} {interest}" for interest in interest_list][:5]
