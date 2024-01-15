import flask
from database_commands import *

dataBase = DataBase()
app = flask.Flask(__name__)

class Server():
    def __init__(self):
        connection, cursor = dataBase.connect_database("database.db")
        dataBase.create_table(connection, cursor, "products", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, description TEXT, count INTEGER")
        dataBase.insert_data(connection, cursor, "products", "name, price, description, count", ("Test", 10.0, "Test", 10))
        
        dataBase.create_table(connection, cursor, "recommended_products", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, description TEXT, count INTEGER")
        dataBase.insert_data(connection, cursor, "recommended_products", "name, price, description, count", ("Test", 10.0, "Test", 10))
        
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
    @app.route("/update_product/<product_id>/<column>=<value>", methods=["PUT"])
    def update_product(product_id, column, value):
        try:
            product_id = int(product_id)
        except ValueError:
            return flask.Response("Invalid id", status=404)
        
        if column not in ["name", "price", "description", "count"]:
            return flask.Response("Column not found", status=404)
        
        if column in ["name", "description"]:
            value = str(value)
            
        elif column in ["price", "count"]:
            try:
                value = float(value)
            except ValueError:
                return flask.Response("Invalid value", status=404)
        
        connection, cursor = dataBase.connect_database("database.db")
        
        dataBase_response = dataBase.select_data(cursor, "products", "*", f"id = {product_id}")
        if dataBase_response == []:
            return flask.Response("Product not found", status=404)
        
        dataBase.update_data(connection, cursor, "products", f"{column} = '{value}'", f"id = {product_id}")
        
        return flask.Response("Product updated", status=200)
    
    
    ################################################################
    #                                                              #    
    #                   Add / Remove products                      #
    #                                                              #
    ################################################################
    @app.route("/add_product/name=<name>&price=<price>&description=<description>&count=<count>", methods=["POST"])
    def add_product(name, price, description, count):
        try:
            price = float(price)
            count = int(count)
        except ValueError:
            return flask.Response("Invalid price or count", status=404)
        
        connection, cursor = dataBase.connect_database("database.db")
        
        dataBase.insert_data(connection, cursor, "products", "name, price, description, count", (name, price, description, count))
        
        return flask.Response("Product added", status=200)
    
    @app.route("/remove_product/<product_id>", methods=["DELETE"])
    def remove_product(product_id):
        try:
            product_id = int(product_id)
        except ValueError:
            return flask.Response("Invalid id", status=404)
        
        connection, cursor = dataBase.connect_database("database.db")
        
        dataBase_response = dataBase.select_data(cursor, "products", "*", f"id = {product_id}")
        if dataBase_response == []:
            return flask.Response("Product not found", status=404)
        
        dataBase.delete_data(connection, cursor, "products", f"id = {product_id}")
        
        return flask.Response("Product removed", status=200)
    
    
    ################################################################
    #                                                              #    
    #                    Recommended products                      #
    #                                                              #
    ################################################################
    @app.route("/get_recommended_products/<recommended_id>", methods=["GET"])
    def get_recommended_products(recommended_id):
        try:
            recommended_id = int(recommended_id)
        except ValueError:
            return flask.Response("Invalid id", status=404)
        
        _, cursor = dataBase.connect_database("database.db")
        
        database_response = dataBase.select_data(cursor, "recommended_products", "*", f"id = {recommended_id}")
        
        if database_response == []:
            return flask.Response("Product not found", status=404)
        
        recommended_products = []
        for product in database_response:
            recommended_products.append({"id": product[0], "name": product[1], "price": product[2], "description": product[3], "count": product[4]})
        
        return flask.jsonify(recommended_products=recommended_products)

    @app.route("/get_all_recommended_products", methods=["GET"])
    def get_all_recommended_products():
        _, cursor = dataBase.connect_database("database.db")
        
        database_response = dataBase.select_data(cursor, "recommended_products", "*", "1")
        
        if database_response == []:
            return flask.Response("Product not found", status=404)
        
        recommended_products = []
        for product in database_response:
            recommended_products.append({"id": product[0], "name": product[1], "price": product[2], "description": product[3], "count": product[4]})
        
        return flask.jsonify(recommended_products=recommended_products)


################################################################
#                                                              #
#                           Main                               #
#                                                              #
################################################################    
if __name__ == "__main__":
    Server = Server()
    app.run(debug=True)