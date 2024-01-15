import flask
from database_commands import *

dataBase = DataBase()
app = flask.Flask(__name__)

class Server():
    @app.route("/insert_data/<table>/<columns>/<data>", methods=["POST"])   
    def insert_data(table, columns, data):
        dataBase.insert_data(dataBase.connect_database("database.db"), table, columns, (data,))
        return "Data inserted"
    
    @app.route("/get_data/<table>/<columns>/<condition>", methods=["GET"])
    def get_data(table, columns, condition):
        return str(dataBase.select_data(dataBase.connect_database("database.db"), table, columns, condition))