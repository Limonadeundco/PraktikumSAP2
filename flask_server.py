import flask
from database_commands import *

dataBase = DataBase()
app = flask.Flask(__name__)

class Server():
    def __init__(self):
        connection, cursor = dataBase.connect_database("database.db")
        dataBase.create_table(connection, cursor, "products", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, description TEXT, count INTEGER")
        dataBase.insert_data(connection, cursor, "products", "name, price, description, count", ("Test", 10.0, "Test", 10))
        
        
    ################################################################
    #                                                              #    
    #               Get products for id                            #
    #                                                              #
    ################################################################
    @app.route("/get_product/<product_id>/<column>", methods=["GET"])
    def get_data(product_id, column):
        try:
            product_id = int(product_id)
        except ValueError:
            return flask.Response("Invalid id", status=404)
        
        if column not in ["name", "price", "description", "count"]:
            return flask.Response("Column not found", status=404)
        
        _, cursor = dataBase.connect_database("database.db")
        
        database_response = dataBase.select_data(cursor, "products", column, f"id = {product_id}")
        
        if database_response == []:
            return flask.Response("Product not found", status=404)
        
        #format response nicely into a good looking json
        return flask.jsonify(database_response)
    
    @app.route("/get_product/<product_id>", methods=["GET"])
    def get_product(product_id):
        try:
            product_id = int(product_id)
        except ValueError:
            return flask.Response("Invalid id", status=404)
        
        _, cursor = dataBase.connect_database("database.db")
        
        database_response = dataBase.select_data(cursor, "products", "*", f"id = {product_id}")
        
        if database_response == []:
            return flask.Response("Product not found", status=404)
        
        return flask.jsonify(product={"id": database_response[0][0], "name": database_response[0][1], "price": database_response[0][2], "description": database_response[0][3], "count": database_response[0][4]})
    
    
    ################################################################
    #                                                              #    
    #                     Get all products                         #
    #                                                              #
    ################################################################
    @app.route("/get_all_products/<limit>", methods=["GET"])
    def get_all_products(limit):
        try:
            limit = int(limit)
        except ValueError:
            return flask.Response("Invalid limit", status=404)
        
        _, cursor = dataBase.connect_database("database.db")
        
        database_response = dataBase.select_data(cursor, "products", "*", f"id < {limit + 1}")
        
        if database_response is None:
            return flask.Response("No Products found", status=404)
        
        response = []
        for product in database_response:
            product = {"product": {"id": product[0], "name": product[1], "price": product[2], "description": product[3], "count": product[4]}}
            response.append(product)
        
        return flask.jsonify(products=response)
    
    @app.route("/get_all_products", methods=["GET"])
    def get_all_products_no_limit():
        _, cursor = dataBase.connect_database("database.db")
        
        database_response = dataBase.select_data(cursor, "products", "*", "1")
        
        if database_response is None:
            return flask.Response("No Products found", status=404)
        
        response = []
        for product in database_response:
            product = {"product": {"id": product[0], "name": product[1], "price": product[2], "description": product[3], "count": product[4]}}
            response.append(product)
        
        return flask.jsonify(products=response)
    
    
    ################################################################
    #                                                              #    
    #                      Update products                         #
    #                                                              #
    ################################################################
    @app.route("/update_product/<product_id>/<column>/<value>", methods=["PUT"])
    def update_product(product_id, column, value):
        try:
            product_id = int(product_id)
        except ValueError:
            return flask.Response("Invalid id", status=404)
        
        if column not in ["name", "price", "description", "count"]:
            return flask.Response("Column not found", status=404)
        
        connection, cursor = dataBase.connect_database("database.db")
        
        database_response = dataBase.update_data(connection, cursor, "products", f"{column} = {value}", f"id = {product_id}")
        
        if database_response == []:
            return flask.Response("Product not found", status=404)
        
        return flask.Response("Product updated", status=200)
    
    
    
if __name__ == "__main__":
    Server = Server()
    app.run(debug=True)