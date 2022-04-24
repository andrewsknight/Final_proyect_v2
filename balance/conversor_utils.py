from traceback import print_tb
from flask import flash, jsonify
import requests
import sqlite3
import balance.api_key
from balance import money_controller

api_key = balance.api_key.api_key4
endpoint = "https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey="+api_key


def invest_eur():
    total_money = 0
    movements = money_controller.get_movements()
    for movement in movements:
        if movement["from_moneda"] == 'EUR':
            total_money += movement["from_cantidad"]
    return total_money

def all_money(currency):
    total_money = 0
    movements = money_controller.get_movements()
    for movement in movements:
        if movement["to_moneda"] == currency:
            total_money += movement["to_cantidad"]
        if movement["from_moneda"] == currency:
            total_money -= movement["from_cantidad"]

    return total_money

def conversor(amount, money_from, money_to):

    try:

        result = requests.get(endpoint.format(money_from, money_to))
        jason = result.json()
        print('-----------------')
        if "error" in jason:
            print('error')
            return -1
        valor_money_from = round(jason["rate"], 4)

    except requests.exceptions.RequestException as e:
        print(e)
        return {
            "status": "failure",
            "message": "Demasiadas peticiones al api, inténtelo de nuevo en 24 horas"
        }

    final_valor = float(amount) * valor_money_from

    return final_valor
