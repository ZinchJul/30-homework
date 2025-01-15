from datetime import datetime

import pytest


@pytest.mark.parametrize('status_code', 200)
@pytest.fixture
def test_client(client) -> None:
    resp = client.get("/client/1")
    assert resp.status_code == 200
    assert resp.json == {"id": 1, "name": "name", "surname": "surname",
                         "credit_card": "credit_card", "car_number": "car_number"}


@pytest.fixture
def test_create_client(client) -> None:
    client_data = {"name": "Никита", "surname": "Нестеренко",
                 "credit_card": "Alfa 2200 ** 6544", "car_number": "р 122 ор 12 rus"}
    resp = client.post("/add_clients", data=client_data)

    assert resp.status_code == 201


@pytest.fixture
def test_create_parking(client) -> None:
    parking_data = {"address": 'Самара, ул. Победы 1/10', "opened": True,
                 "count_places": 200, "count_available_places": 150}
    resp = client.post("/add_clients", data=parking_data)

    assert resp.status_code == 201


@pytest.fixture
def test_parking_in(client):
    parking_in_data = {"client_id": 1, "parking_id": 1,
                    "time_in": datetime.now()}
    resp = client.post("/client_parkings", data=parking_in_data)

    assert resp.status_code == 201


@pytest.fixture
def test_parking_out(client):
    parking_out_data = {"client_id": 1, "parking_id": 1,
                     "time_out": datetime.now()}
    resp = client.post("/clients_parking", data=parking_out_data)

    assert resp.status_code == 201
