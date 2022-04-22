from flask import flash
import requests

endpoint = "https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey=C3A26AE3-1A54-4A04-A692-DF882C9295E5"


def conversor(amount, money_from, money_to):
   

    result = requests.get(endpoint.format(money_from, money_to))
    try:
        valor_money_from = round(result.json()["rate"], 4)
    except:
        print('error', result.json())
    
    final_valor = float(amount) * valor_money_from
    
    return final_valor

    



