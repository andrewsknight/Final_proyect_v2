from crypt import methods
from balance import app
from balance import money_controller
import sqlite3
from flask import jsonify, render_template, request, flash
from balance import conversor_utils
import balance


@app.route("/api/v1/cryptos/diferent", methods=["GET"])
def get_diferent_cryptos():

    try:
        moneys = money_controller.get_diferent_to_money()
        result = {}
        for money in moneys:
            result[money] = ""

        return jsonify({
            "status": "success",
            "data": result

        })
    except sqlite3.Error as e:
        return jsonify({
            "status": "failure",
            "message": "Error en la base de datos, inténtelo de nuevo más tarde"
        }), 400


@app.route("/api/v1/crypto/<crypto>", methods=["GET"])
def get_crypto(crypto):

    try:
        moneys = money_controller.get_diferent_to_money()
        crypto = crypto.upper()
        if crypto not in moneys:
            return jsonify({
                "status:": "failure",
                "message": "introduce una crypto que tengas en la wallet"
            }), 400
        else:

            amount_crypto = conversor_utils.all_money(crypto)
            crypto_money_value = conversor_utils.conversor(
                amount_crypto, crypto, "EUR")

            if crypto_money_value == -1:
                return jsonify({
                    "status": "failure",
                    "message": "Error en la base de datos, inténtelo de nuevo más tarde",
                    "message2": "Demasiadas peticiones al api, inténtelo de nuevo más tarde"
                }), 400
            return jsonify({
                "status": "success",
                "amount": amount_crypto,
                "crypto_money_value": crypto_money_value
            })
    except sqlite3.Error as e:
        return jsonify({
            "status": "failure",
            "message": "Error en la base de datos, inténtelo de nuevo más tarde"
        }), 400


@app.route("/api/v1/movimientos", methods=["GET"])
def get_movements():
    try:
        movements = money_controller.get_movements()
        return jsonify({
            "status": "success",
            "data": movements

        })
    except sqlite3.Error as e:
        return jsonify({
            "status": "failure",
            "message": "Error en la base de datos, inténtelo de nuevo más tarde"
        }), 400


@app.route("/api/v1/movimiento/<id>", methods=["GET"])
def get_movement_by_id(id):
    try:
        movement = money_controller.get_by_id(id)

        return jsonify(movement)
    except sqlite3.Error as e:
        return jsonify({
            "status": "failure",
            "message": "Error en la base de datos, inténtelo de nuevo más tarde"
        }), 400

@app.route("/api/v1/movimiento", methods=["POST"])
def insert_movement():
    try:
        movement = request.get_json()
        if movement:
            if "fecha" in movement:
                fecha = movement["fecha"]
            else:
                return jsonify({
                    "status": "failure",
                    "message": "Debe ingresar una fecha"})

            if "hora" in movement:
                hora = movement["hora"]
            else:
                return jsonify({
                    "status": "failure",
                    "message": "Debe ingresar una hora"})

            if "from_moneda" in movement:
                from_moneda = movement["from_moneda"]
            else:
                return jsonify({
                    "status": "failure",
                    "message": "Debe ingresar una moneda"})

            if "from_cantidad" in movement:
                from_cantidad = float(movement["from_cantidad"])
            else:
                return jsonify({
                    "status": "failure",
                    "message": "Debe ingresar una cantidad"})
            if "to_moneda" in movement:
                to_moneda = movement["to_moneda"]
            else:
                return jsonify({
                    "status": "failure",
                    "message": "Debe ingresar una moneda"})

            if "to_cantidad" in movement:
                to_cantidad = float(movement["to_cantidad"])
            else:
                return jsonify({
                    "status": "failure",
                    "message": "Debe ingresar una cantidad"})

            if from_moneda == "EUR" or conversor_utils.all_money(from_moneda) >= from_cantidad:

                last_id = money_controller.insert_movement(
                    fecha, hora, from_moneda, from_cantidad, to_moneda, to_cantidad)
                euro_money = ["EUR"]
                movements = money_controller.get_movements()

                for movement in movements:
                    if euro_money not in movements:
                        euro_money.extend(movements)

                        return jsonify({
                            "status": "success",
                            "id": last_id,
                            "monedas": euro_money
                        }), 201
            else:
                return jsonify({
                    "status": "fail",
                    "mensaje": "Saldo insuficiente"
                }), 400  # aunque en el pdf pone devolver un 200, me imagino que habrá sido un error y he puesto el 400
        else:
            return jsonify({
                "status": "fail",
                "mensaje": "Debe ingresar los datos del movimiento"
            }), 400

    except sqlite3.Error as e:
        return jsonify({
            "status": "failure",
            "message": "Error en la base de datos, inténtelo de nuevo más tarde"
        }), 400


@ app.route("/api/v1/status", methods=["GET"])
def get_status():
    try:
        invest = conversor_utils.invest_eur()
        diferent_to_money = money_controller.get_diferent_to_money()
        tot_money = 0
        for money in diferent_to_money:
            tot_of_this_money = conversor_utils.all_money(money)

            tot_in_eur = conversor_utils.conversor(
                tot_of_this_money, money, 'EUR')

            if tot_in_eur == -1:
                return jsonify({
                    "status": "failure",
                    "message": "Error en la base de datos, inténtelo de nuevo más tarde",
                    "message2": "Demasiadas peticiones al api, inténtelo de nuevo más tarde"
                }), 400

            tot_money += tot_in_eur

        return jsonify({
            "status": "success",
            "data": {
                "invest": invest,
                "diferent_to_money": diferent_to_money,
                "tot_money": tot_money
            }
        })
    except sqlite3.Error as e:
        return jsonify({
            "status": "fail",
            "mensaje": "Error en la api"
        })

@ app.route("/registro")
def movi_pag():
    return render_template("registro.html")


@ app.route("/")
def principal_pag():
    return render_template("index.html")
