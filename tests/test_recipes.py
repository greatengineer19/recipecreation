import pytest


BASE = "/recipes"


# ── helpers ──────────────────────────────────────────────────────────────────

def create_recipe(
    client,
    title="Fried Rice",
    making_time="15 min",
    serves="3 people",
    ingredients="onion, tomato, seasoning",
    cost=450 ):
    return client.post(BASE + "/", json={
        "title": title,
        "making_time": making_time,
        "serves": serves,
        "ingredients": ingredients,
        "cost": cost
    })


# ── health ────────────────────────────────────────────────────────────────────

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# ── create ────────────────────────────────────────────────────────────────────

def test_create_recipe(client):
    response = create_recipe(client)
    assert response.status_code == 200
    data = response.json()

    created_at = data["recipe"][0]["created_at"]
    updated_at = data["recipe"][0]["updated_at"]

    assert data == {
        'message': 'Recipe successfully created!',
        'recipe': [{
            'cost': 450,
            'created_at': created_at,
            'id': 1,
            'ingredients': 'onion, tomato, seasoning',
            'making_time': '15 min',
            'serves': '3 people',
            'title': 'Fried Rice',
            'updated_at': updated_at}]
    }


def test_create_recipe_missing_title(client):
    response = client.post(BASE + "/", json={"making_time": "15 min",
        "serves": "3 people",
        "ingredients": "onion, tomato, seasoning",
        "cost": "450"})
    assert response.status_code == 422


# ── read ──────────────────────────────────────────────────────────────────────

def test_get_recipe(client):
    created = create_recipe(client).json()
    response = client.get(f"{BASE}/{created['recipe']['id']}")
    assert response.status_code == 200
    assert response.json() == {'message': 'Recipe details by id',
        'recipe': {
            'cost': 450,
            'id': 1,
            'ingredients': 'onion, tomato, seasoning',
            'making_time': '15 min',
            'serves': '3 people',
            'title': 'Fried Rice'
        }
    }


def test_get_recipe_not_found(client):
    response = client.get(f"{BASE}/99999")
    assert response.status_code == 404
    assert response.json() == {'success': False, 'message': 'Recipe with id=99999 not found.', 'detail': None}


def test_list_recipes(client):
    recipe1 = create_recipe(client).json()
    recipe2 = create_recipe(client, title="Fried Dumplings").json()
    response = client.get(BASE + "/")
    assert response.status_code == 200
    assert response.json() == {
        'recipes': [{'cost': 450,
        'id': recipe1['recipe']['id'],
        'ingredients': 'onion, tomato, seasoning',
        'making_time': '15 min',
        'serves': '3 people',
        'title': 'Fried Rice'},
        {'cost': 450,
        'id': recipe2['recipe']['id'],
        'ingredients': 'onion, tomato, seasoning',
        'making_time': '15 min',
        'serves': '3 people',
        'title': 'Fried Dumplings'}]
    }


# ── update ────────────────────────────────────────────────────────────────────

def test_update_item(client):
    recipe = create_recipe(client, title="Old").json()["recipe"]
    response = client.patch(f"{BASE}/{recipe['id']}", json={
        "title": "New",
        "making_time": recipe["making_time"],
        "serves": recipe["serves"],
        "ingredients": recipe["ingredients"],
        "cost": recipe["cost"]
    })
    assert response.status_code == 200
    assert response.json()["recipe"]["title"] == "New"


def test_update_recipe_not_found(client):
    response = client.patch(f"{BASE}/99999", json={
        "title": "New",
        "making_time": "New",
        "serves": "New",
        "ingredients": "New",
        "cost": 100
    })
    assert response.status_code == 404


# ── delete ────────────────────────────────────────────────────────────────────

def test_delete_recipe(client):
    recipe = create_recipe(client, title="Old").json()["recipe"]
    response = client.delete(f"{BASE}/{recipe['id']}")
    assert response.status_code == 200

    response2 = client.get(f"{BASE}/{recipe['id']}")
    assert response2.status_code == 404


def test_delete_recipe_not_found(client):
    response = client.delete(f"{BASE}/99999")
    assert response.status_code == 404
