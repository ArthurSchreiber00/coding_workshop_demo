import re


def test_dashboard_renders(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Übersicht" in resp.text
    assert "Toolshed" in resp.text


def test_dashboard_cards_show_numbers(client):
    html = client.get("/").text
    for label in ("Geräte", "verfügbar", "ausgeliehen", "Personen"):
        match = re.search(r'<div class="card-value">([^<]*)</div><div class="card-label">' + label + "</div>", html)
        assert match, f"Karte {label} fehlt"
        assert match.group(1).strip().isdigit(), f"Karte {label} zeigt keine Zahl: {match.group(1)!r}"
    assert "built-in method" not in html


def test_items_page_with_search(client):
    resp = client.get("/items", params={"q": "Sony"})
    assert resp.status_code == 200
    assert "Sony A7 IV" in resp.text


def test_new_item_form_roundtrip(client):
    resp = client.post(
        "/items/new",
        data={"name": "Testgerät", "category": "Zubehör", "inventory_no": "INV-9100", "notes": ""},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert resp.headers["location"] == "/items"


def test_loan_form_enforces_max_open_loans(client, api_headers):
    # Person 4 (Jonas) hat eine offene Ausleihe aus den Seed-Daten; zwei weitere per API anlegen …
    for item_id in (2, 4):
        r = client.post("/api/loans", json={"item_id": item_id, "member_id": 4}, headers=api_headers)
        assert r.status_code == 201, r.text
    # … die vierte über das Formular muss abgelehnt werden.
    resp = client.post("/loans/new", data={"item_id": 10, "member_id": 4, "due_date": ""})
    assert resp.status_code == 200
    assert "bereits 3 offene Ausleihen" in resp.text
    assert client.get("/api/items/10").json()["status"] == "available"


def test_members_page(client):
    resp = client.get("/members")
    assert resp.status_code == 200
    assert "Aylin Kaya" in resp.text
