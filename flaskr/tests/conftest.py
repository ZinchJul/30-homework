from datetime import datetime

import pytest
from module_29_testing.hw.flaskr.app import create_app
from module_29_testing.hw.models import Client, Parking, Client_Parking
from module_29_testing.hw.models import db as _db



@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"

    with _app.app_context():
        _db.create_all()
        client = Client(id=1,
                    name="name",
                    surname="surname",
                    credit_card='credit_card',
                    car_number='car_number')
        parking = Parking(id=1, address="address",
                          opened=True,
                          count_places=10,
                          count_available_places=2)
        take_parking = Client_Parking(id=1,
                                      client_id=1,
                                      parking_id=1,
                                      time_in=datetime.now(),
                                      time_out=(2025, 2, 2, 11, 41, 17))
        _db.session.add(client)
        _db.session.add(parking)
        _db.session.add(take_parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture(scope='module')
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db