from fastapi import Header

from app import config
from app.errors import ApiError


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Schreibende API-Endpunkte verlangen den Header X-Api-Key."""
    if x_api_key != config.API_KEY:
        raise ApiError(401, "unauthorized", "Ungültiger oder fehlender X-Api-Key.")
