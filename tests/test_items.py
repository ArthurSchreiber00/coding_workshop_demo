def test_list_items_returns_seed_data(client):
    resp = client.get("/api/items")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) >= 10
    assert {"id", "name", "inventory_no", "status"} <= items[0].keys()


def test_filter_by_status(client):
    resp = client.get("/api/items", params={"status": "maintenance"})
    assert resp.status_code == 200
    assert all(i["status"] == "maintenance" for i in resp.json())
    assert len(resp.json()) >= 1


def test_search_items(client):
    resp = client.get("/api/items", params={"q": "Beamer"})
    assert resp.status_code == 200
    assert any("Beamer" in i["name"] for i in resp.json())


def test_get_unknown_item_uses_error_envelope(client):
    resp = client.get("/api/items/9999")
    assert resp.status_code == 404
    assert resp.json() == {"error": {"code": "item_not_found", "message": "Gerät 9999 existiert nicht."}}


def test_create_item_requires_api_key(client):
    resp = client.post("/api/items", json={"name": "X", "category": "Y", "inventory_no": "INV-9001"})
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "unauthorized"


def test_create_and_update_item(client, api_headers):
    payload = {"name": "Dell Monitor 27\"", "category": "Zubehör", "inventory_no": "INV-9002"}
    resp = client.post("/api/items", json=payload, headers=api_headers)
    assert resp.status_code == 201
    item = resp.json()
    assert item["status"] == "available"

    resp = client.patch(f"/api/items/{item['id']}", json={"status": "maintenance"}, headers=api_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "maintenance"


def test_duplicate_inventory_no_is_conflict(client, api_headers):
    payload = {"name": "Doppelt", "category": "Zubehör", "inventory_no": "INV-0001"}
    resp = client.post("/api/items", json=payload, headers=api_headers)
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "inventory_no_taken"


def test_validation_error_uses_error_envelope(client, api_headers):
    resp = client.post("/api/items", json={"name": "", "category": "Y", "inventory_no": "INV-9003"}, headers=api_headers)
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "validation_error"
