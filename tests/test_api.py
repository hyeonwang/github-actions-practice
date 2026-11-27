import pytest
from fastapi.testclient import TestClient

from orderlab.api import create_app


@pytest.fixture
def client():
    with TestClient(create_app()) as client:
        yield client


def test_create_and_get(client):
    response = client.post("/orders", json={"price": 10_000, "quantity": 2})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "subtotal": 20_000}

    response = client.get("/orders/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "subtotal": 20_000}


def test_not_found(client):
    response = client.get("/orders/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}


@pytest.mark.parametrize(
    ("price", "quantity", "field"), [(100, 0, "quantity"), (-1, 2, "price")]
)
def test_invalid_order(client, price, quantity, field):
    response = client.post("/orders", json={"price": price, "quantity": quantity})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", field]
