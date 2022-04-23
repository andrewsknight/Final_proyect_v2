from flask import flash, jsonify
import requests
import sqlite3

endpoint = "https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey=C3A26AE3-1A54-4A04-A692-DF882C9295E5"


def conversor(amount, money_from, money_to):

    try:

        result = requests.get(endpoint.format(money_from, money_to))
        jason = result.json()
        if "error" in jason:
            return -1
        valor_money_from = round(jason["rate"], 4)

    except requests.exceptions.RequestException as e:
        return {
            "status": "failure",
            "message": "Demasiadas peticiones al api, inténtelo de nuevo en 24 horas"
        }

    final_valor = float(amount) * valor_money_from

    return final_valor
