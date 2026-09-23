def test_list_members(client):
    resp = client.get("/api/members")
    assert resp.status_code == 200
    names = {m["name"] for m in resp.json()}
    assert "Dana Berger" in names


def test_member_loans(client):
    resp = client.get("/api/members/2/loans")
    assert resp.status_code == 200
    assert all(l["member_id"] == 2 for l in resp.json())


def test_create_member(client, api_headers):
    payload = {"name": "Neue Person", "email": "neu@example.com", "team": "QA"}
    resp = client.post("/api/members", json=payload, headers=api_headers)
    assert resp.status_code == 201
    assert resp.json()["is_admin"] is False


def test_unknown_member(client):
    resp = client.get("/api/members/9999")
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "member_not_found"


def test_search_members(client):
    resp = client.get("/api/members", params={"q": "kaya"})
    assert resp.status_code == 200
    assert [m["name"] for m in resp.json()] == ["Aylin Kaya"]


def test_search_members_by_team(client):
    names = {m["name"] for m in client.get("/api/members", params={"q": "Frontend"}).json()}
    assert {"Tom Vogel", "Mira Schulz"} <= names
