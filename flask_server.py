import flask
from database_commands import *

dataBase = DataBase()
app = flask.Flask(__name__)

class Server():
    def __init__(self):
        dataBase.create_table(dataBase.connect_database("database.db"), "products", "id INTEGER PRIMARY KEY, name TEXT, price REAL, description TEXT, count INTEGER")
        
    @app.route("/get_product/<product_id>/<column>", methods=["GET"])
    def get_data(product_id, column):
        if column not in ["name", "price", "description", "count"]:
            return flask.Response("Column not found", status=404)
        
        _, cursor = dataBase.connect_database("database.db")
        
        return str(dataBase.select_data(cursor, "products", column, f"id = {product_id}"))
    
if __name__ == "__main__":
    app.run(debug=True)