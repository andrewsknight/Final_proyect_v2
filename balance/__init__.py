from json.tool import main
from flask import Flask
from balance import data_code

app = Flask(__name__, instance_relative_config=True)


from balance import routes

if __name__ == "balance":
    
    data_code.create_tables()

