import flask
import sys
import database_commands.database_commands as database_commands
import cv2
import base64
import recommended_product_functions

rpf = recommended_product_functions.recommended_product_functions()

dataBase = database_commands.DataBase()
app = flask.Flask(__name__)


allowed_columns = ["name", "price", "description", "count"]
string_colums = ["name", "description"]
int_colums = ["price", "count"]

class Server():
    def __init__(self):
        connection, cursor = dataBase.connect_database("database.db")
        dataBase.create_table(connection, cursor, "products", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, description TEXT, count INTEGER, sales INTEGER")
        dataBase.insert_data(connection, cursor, "products", "name, price, description, count", ("Test", 10.0, "Test", 10))
        
        dataBase.create_table(connection, cursor, "sales", "id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, date TEXT, count INTEGER")
        
        dataBase.create_table(connection, cursor, "recommended_products", "id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, sales_last_day INTEGER")
        
        dataBase.create_table(connection, cursor, "images", "id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, image_id INTEGER, image_path TEXT")
        dataBase.insert_data(connection, cursor, "images", "product_id, image_id, image_path", (1, 1, "images/1/1.jpg"))
        
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
        
        if column not in allowed_columns:
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
        
        conn, cursor = dataBase.connect_database("database.db")
        
        database_response = dataBase.select_data(cursor, "products", "*", f"id = {product_id}")
        
        if database_response == []:
            return flask.Response("Product not found", status=404)
        
        # Fetch column names from cursor description
        column_names = [column[0] for column in cursor.description]

        # Create a dictionary for the product using column names
        product = {column_names[i]: database_response[0][i] for i in range(len(column_names))}

        return flask.jsonify(product=product)
    
    
    ################################################################
    #                                                              #    
    #                     Get all products                         #
    #                                                              #
    ################################################################
    @app.route("/get_all_products", defaults={'limit': None}, methods=["GET"])
    @app.route("/get_all_products/<limit>", methods=["GET"])
    def get_all_products(limit):
        if limit is not None:
            try:
                limit = int(limit)
            except ValueError:
                return flask.Response("Invalid limit", status=404)
            query = f"id < {limit + 1}"
        else:
            query = "1"

        _, cursor = dataBase.connect_database("database.db")

        database_response = dataBase.select_data(cursor, "products", "*", query)

        if database_response is None:
            return flask.Response("No Products found", status=404)

        column_names = [column[0] for column in cursor.description]

        response = []
        for y, product in enumerate(database_response):
            product = {'product': {column_names[i]: database_response[y][i] for i in range(len(column_names))}}
            response.append(product)

        return flask.jsonify(products=response)
    
    
    ################################################################
    #                                                              #    
    #                      Update products                         #
    #                                                              #
    ################################################################
    @app.route("/update_product/<product_id>/<parameters>", methods=["PUT"])
    def update_product(product_id, parameters):
        try:
            product_id = int(product_id)
        except ValueError:
            return flask.Response("Invalid id", status=404)

        params = parameters.split('&')
        updates = []
        for param in params:
            column, value = param.split('=')
            if column not in allowed_columns:
                return flask.Response(f"Column {column} not found", status=404)

            if column in string_colums:
                value = str(value)
            elif column in int_colums:
                try:
                    value = float(value)
                except ValueError:
                    return flask.Response("Invalid value", status=404)

            updates.append(f"{column} = '{value}'")

        connection, cursor = dataBase.connect_database("database.db")

        database_response = dataBase.select_data(cursor, "products", "*", f"id = {product_id}")
        if database_response == []:
            return flask.Response("Product not found", status=404)

        for update in updates:
            dataBase.update_data(connection, cursor, "products", update, f"id = {product_id}")

        return flask.Response("Product updated", status=200)
    
    
    ################################################################
    #                                                              #    
    #                   Add / Remove products                      #
    #                                                              #
    ################################################################
    @app.route("/add_product/<path:parameters>", methods=["POST"])
    def add_product(parameters):
        params = parameters.split('&')
        data = {}
        for param in params:
            key, value = param.split('=')
            if key not in allowed_columns:
                return flask.Response(f"Column {key} not found", status=404)
            if key in string_colums:
                value = str(value)
            elif key in int_colums:
                try:
                    value = float(value)
                except ValueError:
                    return flask.Response("Invalid value", status=404)
            data[key] = value

        connection, cursor = dataBase.connect_database("database.db")

        columns = ', '.join(data.keys())
        values = tuple(data.values())

        dataBase.insert_data(connection, cursor, "products", columns, values)

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
    @app.route("/get_recommended_products/<limit>", methods=["GET"])
    @app.route("/get_recommended_products", defaults={'limit': 5}, methods=["GET"])
    def get_recommended_products(limit=5):
        try:
            limit = int(limit)
        except ValueError:
            return flask.Response("Invalid id", status=404)

        connection, cursor = dataBase.connect_database("database.db")
        
        try:
            rpf.generate_recommended_products(connection, cursor, limit)
        except IndexError as e:
            return flask.Response(str(e), status=404)
        
        database_response = dataBase.select_data(cursor, "recommended_products", "*")
        
        if database_response == []:
            return flask.Response("Product not found", status=404)
        
        recommended_products = []
        for product in database_response:
            recommended_products.append({"id": product[0], "product_id": product[1], "sales_last_day": product[2]})
        
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
    #                         Images                               #
    #                                                              #
    ################################################################  
    @app.route("/get_image/<product_id>", methods=["GET"])
    @app.route("/get_image/<product_id>/<image_id>", methods=["GET"])
    def get_image_product(product_id, image_id=None):
        try:
            product_id = int(product_id)
        except ValueError:
            return flask.Response("Invalid id", status=404)
        
        try:
            image_id = int(image_id)
        except ValueError:
            return flask.Response("Invalid image id", status=404)
        except TypeError:
            image_id = 1
        
        _, cursor = dataBase.connect_database("database.db")
        
        database_response = dataBase.select_data(cursor, "images", "*", f"product_id = {product_id} AND id = {image_id}")
        
        if database_response == []:
            return flask.Response("Image not found", status=404)
        
        image_path = database_response[0][3]
        
        cv2_image = cv2.imread(image_path)

        # Convert the image to bytes
        _, buffer = cv2.imencode('.jpg', cv2_image)
        image_bytes = buffer.tobytes()

        # Convert bytes to base64
        base64_image = base64.b64encode(image_bytes).decode()

        # Create a data URL
        data_url = f"data:image/jpeg;base64,{base64_image}"

        return flask.Response(data_url, status=200, mimetype='text/html')
        
    
    #@app.route("/get_image/utility/<name>", methods=["GET"])


################################################################
#                                                              #
#                           Main                               #
#                                                              #
################################################################    
if __name__ == "__main__":
    Server = Server()
    app.run(debug=True)