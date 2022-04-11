from flask import flash
import requests

endpoint = "https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey=E01CCF95-56F6-42CD-9ABA-67E8380016F1"

def conversor(amount, money_from, money_to):
    if not amount:
        return flash("Debes indicar una cantidad")
    else: 
        pass
    result = requests.get(endpoint.format(money_from, money_to))
    
    valor_money_from = round(result.json()["rate"], 4)
    
    final_valor = float(amount) * valor_money_from
    
    return print(final_valor)

    
   

    

conversor(3,"BTC", "SOL")



