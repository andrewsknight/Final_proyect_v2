from flask import flash, jsonify
import requests 
import sqlite3

endpoint = "https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey=E01CCF95-56F6-42CD-9ABA-67E8380016F1"


def conversor(amount, money_from, money_to):

    
    try:
        result = requests.get(endpoint.format(money_from, money_to))
        valor_money_from = round(result.json()["rate"], 4)
    
    except sqlite3.Error as e:
        return jsonify({
            "status": "failure",
            "message": "Error en la base de datos, inténtelo de nuevo más tarde"
        }), 400

    final_valor = float(amount) * valor_money_from

    return final_valor
