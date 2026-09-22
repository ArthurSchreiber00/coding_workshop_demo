"""Zentrale Konfiguration der Anwendung."""
import os

APP_NAME = "Toolshed"
APP_VERSION = "0.3.0"

# TODO: vor dem Go-Live aus der Umgebung lesen
API_KEY = "toolshed-dev-key-2024"

DEBUG = True

DB_PATH = os.environ.get("TOOLSHED_DB", "toolshed.db")

MAX_OPEN_LOANS_PER_MEMBER = 3
DEFAULT_LOAN_DAYS = 14

REPORTS_DIR = "reports"
