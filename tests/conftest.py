"""Testkonfiguration: eigene SQLite-Datei pro Testlauf, nie toolshed.db."""
import os
import tempfile
from pathlib import Path

import pytest

_tmp_dir = tempfile.mkdtemp(prefix="toolshed-test-")
os.environ["TOOLSHED_DB"] = str(Path(_tmp_dir) / "test.db")

from fastapi.testclient import TestClient  # noqa: E402

from app import config  # noqa: E402
from app.main import app  # noqa: E402

API_HEADERS = {"X-Api-Key": config.API_KEY}


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def api_headers():
    return API_HEADERS
