from flask import Flask
from flaskr.routes import register_routes

from models import Client, Parking, db

data_add_clients = (
    Client(
        name="Ivan",
        surname="Petrov",
        credit_card="Sber 2200 ** 4455",
        car_number="o 654 кп 63 rus",
    ),
    Client(
        name="Svetlana",
        surname="Sergeeva",
        credit_card="VTB 2200 ** 1234",
        car_number="у 574 лд 74 rus",
    ),
)

data_add_parkings = (
    Parking(
        address="Самара, ул.Парковая, 1д",
        opened=True,
        count_places=50,
        count_available_places=50,
    ),
    Parking(
        address="Самара, ул.Съездовская, 15",
        opened=True,
        count_places=150,
        count_available_places=150,
    ),
)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking_free.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        for item in data_add_clients:
            db.session.add(item)
        for i in data_add_parkings:
            db.session.add(i)
        db.session.commit()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    register_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
