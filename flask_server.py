import flask
from database_commands import *

dataBase = DataBase()
app = flask.Flask(__name__)

class Server():
    def __init__(self):
        connection, cursor = dataBase.connect_database("database.db")
        dataBase.create_table(connection, cursor, "products", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, description TEXT, count INTEGER")
        dataBase.insert_data(connection, cursor, "products", "name, price, description, count", ("Test", 10.0, "Test", 10))
        
    @app.route("/get_product/<product_id>/<column>", methods=["GET"])
    def get_data(product_id, column):
        print(column)
        if column not in ["name", "price", "description", "count"]:
            return flask.Response("Column not found", status=404)
        
        _, cursor = dataBase.connect_database("database.db")
        
        database_response = dataBase.select_data(cursor, "products", column, f"id = {product_id}")
        
        if database_response is None:
            return flask.Response("Product or column not found", status=199)
        
        #format response nicely into a good looking json
        return flask.jsonify(database_response)
    
    @app.route("/get_product/<product_id>", methods=["GET"])
    def get_product(product_id):
        _, cursor = dataBase.connect_database("database.db")
        
        database_response = dataBase.select_data(cursor, "products", "*", f"id = {product_id}")
        
        if database_response is None:
            return flask.Response("Product or column not found", status=199)
        
        return flask.jsonify(database_response)
    
if __name__ == "__main__":
    Server = Server()
    app.run(debug=True)