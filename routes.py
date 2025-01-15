from flask import request, jsonify
from datetime import datetime
from models import db, Client, Client_Parking, Parking


def register_routes(app):
    @app.route('/clients', methods=['GET'])
    def get_all_clients():

        result = db.session.execute(db.select(Client).order_by(Client.surname))
        clients = result.scalars()
        list_clients = []
        for client in clients:
            list_clients.append(client.to_json())
        db.session.commit()
        return jsonify(list_clients), 200


    @app.route('/clients/<int:client_id>', methods=['GET'])
    def get_client_by_id(client_id: int):
        client: Client = db.session.get(Client, client_id)
        if client is None:
            return jsonify({'error': 'Client not found'}), 404
        return jsonify(client.to_json()), 200


    @app.route('/add_clients', methods=['POST'])
    def add_client():
        client = Client(name=request.form["name"], surname=request.form["surname"], credit_card=request.form["credit_card"],
                        car_number=request.form["car_number"])
        db.session.add(client)
        db.session.commit()

        return "Клиент успешно добавлен", 201


    @app.route('/parkings', methods=['POST'])
    def parkings():
        parking = Parking(address=request.form["address"], opened=request.form["opened"],
                          count_places=request.form["count_places"],
                          count_available_places=request.form["count_available_places"])
        db.session.add(parking)
        db.session.commit()

        return "Паркинг успешно добавлен", 201


    @app.route('/client_parkings', methods=['POST'])
    def client_in_parking():
        data = request.get_json()
        client = db.session.get(Client, data['client_id'])
        open_parking = db.session.get(Parking, data['parking_id'])
        if client is None or open_parking is None:
            return jsonify({'error': 'Client or Parking not found'}), 404

        if open_parking.opened:
            if open_parking.count_available_places > 0 and client.credit_card is not None:
                count_available_places = open_parking.count_available_places
                count_available_places -= 1
                open_parking.count_available_places = count_available_places
                take_place_parking = Client_Parking(client_id=client.id,
                                                    parking_id=open_parking.id,
                                                    time_in=datetime.now())
                db.session.add(take_place_parking)
                db.session.commit()
                return jsonify(take_place_parking.to_json()), 201

            else:
                return jsonify({'error': 'no available places '
                                         'or client has no credit card'
                                     }), 400
        else:
            return jsonify({'error': 'Parking is closed'
                                     }), 400


    @app.route("/clients_parking", methods=['DELETE'])
    def client_parking_out():

        data = request.get_json()
        client_parking = db.session.query(Client_Parking).filter_by(
            client_id=data['client_id'],
            parking_id=data['parking_id']
        ).first()
        if client_parking is None:
            return jsonify({'error': 'Client Parking not found'}), 404

        client_parking.time_out = datetime.now()
        parking = db.session.get(Parking, data['parking_id'])
        parking.count_available_places += 1
        db.session.commit()
        return jsonify(client_parking.to_json())
