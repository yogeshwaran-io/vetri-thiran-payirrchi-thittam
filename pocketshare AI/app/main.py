from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.config import get_settings
from app.database import Base, engine
from app.routers import auth, history, planners

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="PocketShare AI planner and recommendation API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(planners.router)
app.include_router(history.router)


@app.get("/", response_model=None)
def read_root(request: Request) -> dict[str, str] | HTMLResponse:
    accept_header = (request.headers.get("accept") or "").lower()
    if "text/html" in accept_header:
        return HTMLResponse(
            content=f"""
            <!DOCTYPE html>
            <html lang=\"en\">
            <head>
                <meta charset=\"utf-8\" />
                <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
                <title>{settings.app_name}</title>
                <style>
                    body {{
                        margin: 0;
                        font-family: Arial, sans-serif;
                        background: #f5f5f5;
                        color: #111827;
                    }}
                    .container {{
                        max-width: 760px;
                        margin: 3rem auto;
                        padding: 2rem;
                        background: white;
                        border-radius: 12px;
                        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
                    }}
                    h1 {{ margin-top: 0; }}
                    code {{
                        display: block;
                        margin-top: 1rem;
                        padding: 1rem;
                        background: #111827;
                        color: #f9fafb;
                        border-radius: 8px;
                        white-space: pre-wrap;
                    }}
                </style>
            </head>
            <body>
                <div class=\"container\">
                    <h1>{settings.app_name}</h1>
                    <p>API is running normally.</p>
                    <code>{{"app": "{settings.app_name}", "status": "ok"}}</code>
                </div>
            </body>
            </html>
            """.strip()
        )
    return {"app": settings.app_name, "status": "ok"}


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
