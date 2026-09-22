from datetime import date, timedelta


def test_list_open_loans(client):
    resp = client.get("/api/loans", params={"open": "true"})
    assert resp.status_code == 200
    loans = resp.json()
    assert loans
    assert all(l["returned_at"] is None for l in loans)
    assert "item_name" in loans[0] and "member_name" in loans[0]


def test_create_loan_requires_api_key(client):
    resp = client.post("/api/loans", json={"item_id": 2, "member_id": 1})
    assert resp.status_code == 401


def test_create_and_return_loan(client, api_headers):
    due = (date.today() + timedelta(days=7)).isoformat()
    resp = client.post("/api/loans", json={"item_id": 7, "member_id": 4, "due_date": due}, headers=api_headers)
    assert resp.status_code == 201
    loan = resp.json()
    assert loan["due_date"] == due
    assert client.get("/api/items/7").json()["status"] == "on_loan"

    resp = client.post(f"/api/loans/{loan['id']}/return", headers=api_headers)
    assert resp.status_code == 200
    assert resp.json()["returned_at"] == date.today().isoformat()
    assert client.get("/api/items/7").json()["status"] == "available"

    resp = client.post(f"/api/loans/{loan['id']}/return", headers=api_headers)
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "already_returned"


def test_cannot_loan_unavailable_item(client, api_headers):
    resp = client.post("/api/loans", json={"item_id": 6, "member_id": 1}, headers=api_headers)
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "item_not_available"


def test_due_date_in_past_is_rejected(client, api_headers):
    resp = client.post("/api/loans", json={"item_id": 9, "member_id": 1, "due_date": "2020-01-01"}, headers=api_headers)
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "due_date_in_past"


def test_unknown_loan(client):
    resp = client.get("/api/loans/9999")
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "loan_not_found"
