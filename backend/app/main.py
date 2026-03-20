"""FastAPI application entry point for Genesis Studio backend.

Product: P001 — PRD-first platform for bot/backend generation and GitHub delivery
"""
from fastapi import FastAPI

from backend.app.api.v1.router import api_v1_router

app = FastAPI(
    title="Genesis Studio",
    description="PRD-first platform for bot/backend generation and GitHub delivery",
    version="0.1.0",
)

app.include_router(api_v1_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "genesis-studio-backend"}
