"""Toolshed – Einstiegspunkt der FastAPI-Anwendung."""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import config, db
from app.errors import register_error_handlers
from app.routers import items, loans, members, pages, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.run_migrations()
    yield


app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    description="Geräteausleihe für Teams. Schreibende Endpunkte verlangen den Header `X-Api-Key`.",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")

app.include_router(pages.router)
app.include_router(items.router)
app.include_router(members.router)
app.include_router(loans.router)
app.include_router(reports.router)

register_error_handlers(app)
