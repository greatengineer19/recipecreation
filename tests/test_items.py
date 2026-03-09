import pytest


BASE = "/items"


# ── helpers ──────────────────────────────────────────────────────────────────

def create_item(client, name="Widget", price="9.99"):
    return client.post(BASE + "/", json={"name": name, "price": price})


# ── health ────────────────────────────────────────────────────────────────────

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# ── create ────────────────────────────────────────────────────────────────────

def test_create_item(client):
    r = create_item(client)
    assert r.status_code == 201
    data = r.json()
    assert data["success"] is True
    assert data["data"]["name"] == "Widget"
    assert float(data["data"]["price"]) == pytest.approx(9.99, rel=1e-4)


def test_create_item_missing_price(client):
    r = client.post(BASE + "/", json={"name": "Oops"})
    assert r.status_code == 422
    assert r.json()["success"] is False


def test_create_item_negative_price(client):
    r = client.post(BASE + "/", json={"name": "Bad", "price": "-1"})
    assert r.status_code == 422


# ── read ──────────────────────────────────────────────────────────────────────

def test_get_item(client):
    created = create_item(client, name="Gadget").json()["data"]
    r = client.get(f"{BASE}/{created['id']}")
    assert r.status_code == 200
    assert r.json()["data"]["name"] == "Gadget"


def test_get_item_not_found(client):
    r = client.get(f"{BASE}/99999")
    assert r.status_code == 404
    assert r.json()["success"] is False


def test_list_items(client):
    create_item(client, name="A")
    create_item(client, name="B")
    r = client.get(BASE + "/")
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is True
    assert body["total"] >= 2
    assert isinstance(body["data"], list)


def test_list_items_pagination(client):
    for i in range(5):
        create_item(client, name=f"Pager{i}")
    r = client.get(BASE + "/?page=1&page_size=2")
    assert r.status_code == 200
    assert len(r.json()["data"]) == 2


# ── update ────────────────────────────────────────────────────────────────────

def test_update_item(client):
    item = create_item(client, name="Old").json()["data"]
    r = client.patch(f"{BASE}/{item['id']}", json={"name": "New", "price": "19.99"})
    assert r.status_code == 200
    assert r.json()["data"]["name"] == "New"


def test_update_item_not_found(client):
    r = client.patch(f"{BASE}/99999", json={"name": "Ghost"})
    assert r.status_code == 404


# ── delete ────────────────────────────────────────────────────────────────────

def test_delete_item(client):
    item = create_item(client, name="ToDelete").json()["data"]
    r = client.delete(f"{BASE}/{item['id']}")
    assert r.status_code == 204

    r2 = client.get(f"{BASE}/{item['id']}")
    assert r2.status_code == 404


def test_delete_item_not_found(client):
    r = client.delete(f"{BASE}/99999")
    assert r.status_code == 404
