"""Toolshed MCP-Server.

Stellt die Toolshed-REST-API als MCP-Tools bereit (Transport: Streamable HTTP, nur localhost).
Start:  python mcp_server/server.py          (App muss auf http://127.0.0.1:8000 laufen)
VS Code: .vscode/mcp.json → Server "toolshed" → Start
"""
import logging
import os
import sys
from datetime import date
from pathlib import Path

import httpx
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from app import config  # noqa: E402

API_URL = os.environ.get("TOOLSHED_API_URL", "http://127.0.0.1:8000")
PORT = int(os.environ.get("TOOLSHED_MCP_PORT", "8001"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
log = logging.getLogger("toolshed-mcp")

mcp = MCPServer(
    "Toolshed",
    instructions="Tools für die Geräteausleihe Toolshed. Schreibende Tools ändern echte Daten der lokalen App.",
)


def _client() -> httpx.Client:
    return httpx.Client(base_url=API_URL, headers={"X-Api-Key": config.API_KEY}, timeout=10.0)


def _call(method: str, path: str, **kwargs):
    with _client() as client:
        resp = client.request(method, path, **kwargs)
    if resp.status_code >= 400:
        try:
            err = resp.json()["error"]
            detail = f"{err['code']}: {err['message']}"
        except (ValueError, KeyError):
            detail = f"HTTP {resp.status_code}: {resp.text[:200]}"
        raise ToolError(detail)
    if resp.status_code == 204:
        return None
    return resp.json()


# --- Tools -----------------------------------------------------------------


@mcp.tool()
def list_items(status: str | None = None) -> list[dict]:
    """Listet alle Geräte. Optionaler Filter status: available | on_loan | maintenance."""
    params = {"status": status} if status else {}
    return _call("GET", "/api/items", params=params)


@mcp.tool()
def search_items(query: str) -> list[dict]:
    """Sucht Geräte nach Name, Inventarnummer oder Kategorie (Teilstring)."""
    return _call("GET", "/api/items", params={"q": query})


@mcp.tool()
def get_item(item_id: int) -> dict:
    """Liefert ein Gerät anhand seiner ID."""
    return _call("GET", f"/api/items/{item_id}")


@mcp.tool()
def list_members() -> list[dict]:
    """Listet alle Personen (Name, Team, E-Mail, Admin-Flag)."""
    return _call("GET", "/api/members")


@mcp.tool()
def list_loans(open_only: bool = True) -> list[dict]:
    """Listet Ausleihen mit Geräte- und Personennamen. open_only=True zeigt nur nicht zurückgegebene."""
    return _call("GET", "/api/loans", params={"open": str(open_only).lower()})


@mcp.tool()
def list_overdue_loans() -> list[dict]:
    """Listet offene Ausleihen, deren Rückgabedatum vor heute liegt, inklusive Anzahl Tage überfällig."""
    today = date.today()
    result = []
    for loan in _call("GET", "/api/loans", params={"open": "true"}):
        due = date.fromisoformat(loan["due_date"])
        if due < today:
            result.append({**loan, "days_overdue": (today - due).days})
    return sorted(result, key=lambda l: l["days_overdue"], reverse=True)


@mcp.tool()
def create_loan(item_id: int, member_id: int, due_date: str | None = None) -> dict:
    """Leiht ein verfügbares Gerät an eine Person aus. due_date im Format YYYY-MM-DD (Standard: heute + 14 Tage)."""
    payload = {"item_id": item_id, "member_id": member_id}
    if due_date:
        payload["due_date"] = due_date
    return _call("POST", "/api/loans", json=payload)


@mcp.tool()
def return_loan(loan_id: int) -> dict:
    """Markiert eine Ausleihe als zurückgegeben und setzt das Gerät auf verfügbar."""
    return _call("POST", f"/api/loans/{loan_id}/return")


# --- Ressourcen & Prompts ----------------------------------------------------


@mcp.resource("toolshed://conventions")
def conventions() -> str:
    """Die Projektkonventionen (docs/conventions.md)."""
    return (ROOT / "docs" / "conventions.md").read_text(encoding="utf-8")


@mcp.resource("toolshed://schema")
def schema() -> str:
    """Das Datenbankschema (app/migrations/001_init.sql)."""
    return (ROOT / "app" / "migrations" / "001_init.sql").read_text(encoding="utf-8")


@mcp.prompt()
def weekly_report() -> str:
    """Wochenbericht über Ausleihen und überfällige Geräte erstellen."""
    return (
        "Erstelle einen kurzen Wochenbericht für das Team: Wie viele Geräte sind ausgeliehen, "
        "welche Ausleihen sind überfällig (mit Person und Tagen), welche Geräte sind in Wartung? "
        "Nutze die Toolshed-Tools und formatiere das Ergebnis als Markdown mit einer Tabelle."
    )


if __name__ == "__main__":
    log.info("Toolshed MCP läuft auf http://127.0.0.1:%s/mcp (API: %s)", PORT, API_URL)
    mcp.run(transport="streamable-http", host="127.0.0.1", port=PORT)
