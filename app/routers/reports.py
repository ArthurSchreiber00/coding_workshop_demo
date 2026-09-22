"""Download von Berichten aus dem reports/-Ordner."""
import os

from fastapi import APIRouter
from fastapi.responses import FileResponse

from app import config
from app.errors import ApiError

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("")
def list_reports():
    names = sorted(n for n in os.listdir(config.REPORTS_DIR) if not n.startswith("."))
    return {"reports": names}


@router.get("/{name:path}")
def download_report(name: str):
    path = os.path.join(config.REPORTS_DIR, name)
    if not os.path.isfile(path):
        raise ApiError(404, "report_not_found", f"Bericht {name} existiert nicht.")
    return FileResponse(path, filename=os.path.basename(path))
