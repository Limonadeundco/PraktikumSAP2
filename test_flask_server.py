import unittest
import flask_server
import os
import database_commands.database_commands as database_commands
import sqlite3
import recommended_product_functions as recommended_product_functions
from datetime import datetime
from PIL import Image
from io import BytesIO
from flask_server import app, dataBase
import time
import uuid

current_year = datetime.now().year
current_month = datetime.now().month

class TestFlaskServer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        #delete database and reset everything 
        cls.conn, cls.cursor = database_commands.DataBase().connect_database("database.db")
        database_commands.DataBase().drop_table(cls.conn, cls.cursor, "products")
        database_commands.DataBase().create_table(cls.conn, cls.cursor, "products", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, description TEXT, count INTEGER, sales INTEGER")
        database_commands.DataBase().drop_table(cls.conn, cls.cursor, "images")
        database_commands.DataBase().create_table(cls.conn, cls.cursor, "images", "id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, image_id INTEGER, image_path TEXT")
        
    @classmethod
    def tearDownClass(cls):
        cls.conn, cls.cursor = database_commands.DataBase().connect_database("database.db")
        #database_commands.DataBase().drop_table(cls.conn, cls.cursor, "products")
        cls.conn.close()
        cls.conn = None
        cls.cursor = None
        
    
    def setUp(self):
        self.app = flask_server.app.test_client()
        self.Server = flask_server.Server()
        self.app.testing = True
        self.conn, self.cursor = database_commands.DataBase().connect_database("database.db")
        database_commands.DataBase().drop_table(self.conn, self.cursor, "products")
        database_commands.DataBase().create_table(self.conn, self.cursor, "products", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, description TEXT, count INTEGER")

    
    def test_add_product(self):
        response = self.app.post("/add_product/name=test_data&price=1.0&description=test_data_desc&count=1")
        self.assertEqual(response.data, b"Product added")
        self.assertEqual(response.status_code, 200)
        
        response = self.app.post("/add_product/name=test_data&price=1.0&description=test_data_desc&count=1")
        self.assertEqual(response.data, b"Product added")
        self.assertEqual(response.status_code, 200)
        
        response = self.app.post("/add_product/name=test_data&price=1.0&description=test_data_desc&count=invalid_value")
        self.assertEqual(response.data, b"Invalid value")
        self.assertEqual(response.status_code, 404)
        
        response = self.app.post("/add_product/name=test_data&price=1.0&description=test_data_desc&count=1&invalid_column=invalid_value")
        self.assertEqual(response.data, b"Column invalid_column not found")
        self.assertEqual(response.status_code, 404)
        
        response = self.app.post("/add_product/name=test_data&price=1.0&description=test_data_desc&count=1&invalid_column=invalid_value&invalid_column2=invalid_value2")
        self.assertEqual(response.data, b"Column invalid_column not found")
        self.assertEqual(response.status_code, 404)
        
        response = self.app.post("/add_product/name=test_data&price=1.0&description=test_data_desc&count=1&invalid_column=invalid_value&invalid_column2=invalid_value2&invalid_column3=invalid_value3")
        self.assertEqual(response.data, b"Column invalid_column not found")
        self.assertEqual(response.status_code, 404)
        
        response = self.app.post("/add_product/name=test_data")
        self.assertEqual(response.data, b"Product added")
        self.assertEqual(response.status_code, 200)
        

    def test_get_data(self):
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data", 1.0, "test_data_desc", 1))
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 1, price = 1.0, name = 'test_data', description = 'test_data_desc'", "id = 1")
        database_commands.DataBase().delete_data(self.conn, self.cursor, "products", "id = 999")
        response = self.app.get("/get_product/1/count")
        try:
            self.assertEqual(response.data, b'[[1]]\n')  # expect a tuple with an integer
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        self.assertEqual(response.status_code, 200)
        
        response = self.app.get("/get_product/1/price")
        try:
            self.assertEqual(response.data, b'[[1.0]]\n')
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        self.assertEqual(response.status_code, 200)
        
        response = self.app.get("/get_product/1/name")
        try:
            self.assertEqual(response.data, b'[["test_data"]]\n')
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        self.assertEqual(response.status_code, 200)
        
        response = self.app.get("/get_product/1/description")
        try:
            self.assertEqual(response.data, b'[["test_data_desc"]]\n')
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        self.assertEqual(response.status_code, 200)
        
        response = self.app.get("/get_product/1/invalid_column")
        try:
            self.assertEqual(response.data, b"Column not found")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        self.assertEqual(response.status_code, 404)
        
        response = self.app.get("/get_product/invalid_id/count")
        try:
            self.assertEqual(response.data, b"Invalid id")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        self.assertEqual(response.status_code, 404)
        
        response = self.app.get("/get_product/999/count")
        try:
            self.assertEqual(response.data, b"Product not found")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
    def test_recommended_products(self):
        self.recommended_product_functions = recommended_product_functions
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.dataBase = database_commands.DataBase()
        
        self.dataBase.drop_table(self.connection, self.cursor, "sales")
        self.dataBase.drop_table(self.connection, self.cursor, "recommended_products")
        self.dataBase.drop_table(self.connection, self.cursor, "products")
        
        self.dataBase.create_table(self.connection, self.cursor, "sales", "id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, sale_time TEXT, count INTEGER")
        
        self.dataBase.create_table(self.connection, self.cursor, "recommended_products", "id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, sales_last_day INTEGER")
        
        self.dataBase.create_table(self.connection, self.cursor, "products", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, description TEXT, count INTEGER, sales INTEGER")
        
        self.dataBase.clear_table(self.connection, self.cursor, "sales")
        self.dataBase.clear_table(self.connection, self.cursor, "recommended_products")
        self.dataBase.clear_table(self.connection, self.cursor, "products")
        
        #generate test data
        self.dataBase.insert_data(self.connection, self.cursor, "products", "name, price, description, count, sales", ("test_product_1", 100, "test_description_1", 10, 0,))
        self.dataBase.insert_data(self.connection, self.cursor, "products", "name, price, description, count, sales", ("test_product_2", 200, "test_description_2", 20, 0,))
        self.dataBase.insert_data(self.connection, self.cursor, "products", "name, price, description, count, sales", ("test_product_3", 300, "test_description_3", 30, 0,))
        self.dataBase.insert_data(self.connection, self.cursor, "products", "name, price, description, count, sales", ("test_product_4", 400, "test_description_4", 40, 0,))
        self.dataBase.insert_data(self.connection, self.cursor, "products", "name, price, description, count, sales", ("test_product_5", 500, "test_description_5", 50, 0,))
        
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (1, f"{current_year}-{current_month}-16 00:10:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (1, f"{current_year}-{current_month}-16 00:30:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (2, f"{current_year}-{current_month}-16 00:50:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (2, f"{current_year}-{current_month}-16 00:00:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (2, f"{current_year}-{current_month}-16 00:20:00", 1,))

        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (2, f"{current_year}-{current_month}-16 00:30:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (2, f"{current_year}-{current_month}-16 00:50:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (2, f"{current_year}-{current_month}-16 00:40:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (3, f"{current_year}-{current_month}-16 00:00:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (3, f"{current_year}-{current_month}-16 00:20:00", 1,))

        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (3, f"{current_year}-{current_month}-16 00:10:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (4, f"{current_year}-{current_month}-16 00:40:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (4, f"{current_year}-{current_month}-16 00:30:00", 1,))
        
        response = self.app.get("/get_recommended_products/5")
        #print("response.data: ", response.data)
        try:
            self.assertEqual(response.data, b'{"recommended_products":[{"id":1,"product_id":2,"sales_last_day":6},{"id":2,"product_id":3,"sales_last_day":3},{"id":3,"product_id":1,"sales_last_day":2},{"id":4,"product_id":4,"sales_last_day":2},{"id":5,"product_id":5,"sales_last_day":0}]}\n')
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        self.assertEqual(response.status_code, 200)
        
        response = self.app.get("/get_recommended_products/3")
        try:
            #print(response.data)
            self.assertEqual(response.data, b'{"recommended_products":[{"id":6,"product_id":2,"sales_last_day":6},{"id":7,"product_id":3,"sales_last_day":3},{"id":8,"product_id":1,"sales_last_day":2}]}\n')
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        self.assertEqual(response.status_code, 200)
        
        response = self.app.get("/get_recommended_products/-1")
        try:
            self.assertEqual(response.data, b'Product count must be bigger than 0')
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        self.assertEqual(response.status_code, 404)
        
        response = self.app.get("/get_recommended_products/invalid_value")
        try:
            self.assertEqual(response.data, b"Invalid id")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        self.assertEqual(response.status_code, 404)
        
        response = self.app.get("/get_recommended_products")
        try:
            self.assertEqual(response.data, b'{"recommended_products":[{"id":9,"product_id":2,"sales_last_day":6},{"id":10,"product_id":3,"sales_last_day":3},{"id":11,"product_id":1,"sales_last_day":2},{"id":12,"product_id":4,"sales_last_day":2},{"id":13,"product_id":5,"sales_last_day":0}]}\n')
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        self.assertEqual(response.status_code, 200)
        
        
        
    def test_get_all_products(self):
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data", 1.0, "test_data_desc", 1))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data4", 1.0, "test_data_desc4", 4))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data2", 1.0, "test_data_desc2", 2))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data3", 1.0, "test_data_desc3", 3))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data5", 1.0, "test_data_desc5", 5))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data6", 1.0, "test_data_desc6", 6))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data7", 1.0, "test_data_desc7", 7))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data8", 1.0, "test_data_desc8", 8))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data9", 1.0, "test_data_desc9", 9))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data10", 1.0, "test_data_desc10", 10))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data11", 1.0, "test_data_desc11", 11))
        
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 1, price = 1.0, name = 'test_data', description = 'test_data_desc'", "id = 1")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 4, price = 1.0, name = 'test_data4', description = 'test_data_desc4'", "id = 2")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 2, price = 1.0, name = 'test_data2', description = 'test_data_desc2'", "id = 3")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 3, price = 1.0, name = 'test_data3', description = 'test_data_desc3'", "id = 4")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 5, price = 1.0, name = 'test_data5', description = 'test_data_desc5'", "id = 5")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 6, price = 1.0, name = 'test_data6', description = 'test_data_desc6'", "id = 6")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 7, price = 1.0, name = 'test_data7', description = 'test_data_desc7'", "id = 7")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 8, price = 1.0, name = 'test_data8', description = 'test_data_desc8'", "id = 8")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 9, price = 1.0, name = 'test_data9', description = 'test_data_desc9'", "id = 9")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 10, price = 1.0, name = 'test_data10', description = 'test_data_desc10'", "id = 10")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 11, price = 1.0, name = 'test_data11', description = 'test_data_desc11'", "id = 11")
        
        expected_data = b'{"products":[{"product":{"count":1,"description":"test_data_desc","id":1,"name":"test_data","price":1.0}},{"product":{"count":4,"description":"test_data_desc4","id":2,"name":"test_data4","price":1.0}},{"product":{"count":2,"description":"test_data_desc2","id":3,"name":"test_data2","price":1.0}},{"product":{"count":3,"description":"test_data_desc3","id":4,"name":"test_data3","price":1.0}},{"product":{"count":5,"description":"test_data_desc5","id":5,"name":"test_data5","price":1.0}},{"product":{"count":6,"description":"test_data_desc6","id":6,"name":"test_data6","price":1.0}},{"product":{"count":7,"description":"test_data_desc7","id":7,"name":"test_data7","price":1.0}},{"product":{"count":8,"description":"test_data_desc8","id":8,"name":"test_data8","price":1.0}},{"product":{"count":9,"description":"test_data_desc9","id":9,"name":"test_data9","price":1.0}},{"product":{"count":10,"description":"test_data_desc10","id":10,"name":"test_data10","price":1.0}}]}\n'
        
        
        response = self.app.get("/get_all_products/10")
        #print(response.data)
        try:
            self.assertEqual(response.data, expected_data)
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
        self.assertEqual(response.status_code, 200)
        
        expected_data = b'{"products":[{"product":{"count":1,"description":"test_data_desc","id":1,"name":"test_data","price":1.0}},{"product":{"count":4,"description":"test_data_desc4","id":2,"name":"test_data4","price":1.0}},{"product":{"count":2,"description":"test_data_desc2","id":3,"name":"test_data2","price":1.0}},{"product":{"count":3,"description":"test_data_desc3","id":4,"name":"test_data3","price":1.0}},{"product":{"count":5,"description":"test_data_desc5","id":5,"name":"test_data5","price":1.0}},{"product":{"count":6,"description":"test_data_desc6","id":6,"name":"test_data6","price":1.0}},{"product":{"count":7,"description":"test_data_desc7","id":7,"name":"test_data7","price":1.0}},{"product":{"count":8,"description":"test_data_desc8","id":8,"name":"test_data8","price":1.0}},{"product":{"count":9,"description":"test_data_desc9","id":9,"name":"test_data9","price":1.0}},{"product":{"count":10,"description":"test_data_desc10","id":10,"name":"test_data10","price":1.0}},{"product":{"count":11,"description":"test_data_desc11","id":11,"name":"test_data11","price":1.0}}]}\n'
        
        response = self.app.get("/get_all_products")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
        
        
    def test_get_product(self):
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data", 1.0, "test_data_desc", 1))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data4", 1.0, "test_data_desc4", 4))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data2", 1.0, "test_data_desc2", 2))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data3", 1.0, "test_data_desc3", 3))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "products", "name, price, description, count", ("test_data5", 1.0, "test_data_desc5", 5))
        
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 1, price = 1.0, name = 'test_data', description = 'test_data_desc'", "id = 1")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 4, price = 1.0, name = 'test_data4', description = 'test_data_desc4'", "id = 2")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 2, price = 1.0, name = 'test_data2', description = 'test_data_desc2'", "id = 3")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 3, price = 1.0, name = 'test_data3', description = 'test_data_desc3'", "id = 4")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 5, price = 1.0, name = 'test_data5', description = 'test_data_desc5'", "id = 5")
        
        response = self.app.get("/get_product/1")
        try:
            self.assertEqual(response.data, b'{"product":{"count":1,"description":"test_data_desc","id":1,"name":"test_data","price":1.0}}\n')
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        self.assertEqual(response.status_code, 200)
        
        response = self.app.get("/get_product/999")
        try:
            self.assertEqual(response.data, b"Product not found")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        self.assertEqual(response.status_code, 404)
        
        response = self.app.get("/get_product/invalid_id")
        try:
            self.assertEqual(response.data, b"Invalid id")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        self.assertEqual(response.status_code, 404)
    
    def test_update_product(self):
        
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "products", "id, name, price, description, count", (1, "test_data", 1.0, "test_data_desc", 1))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "products", "id, name, price, description, count", (4, "test_data4", 1.0, "test_data_desc4", 4))
        
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 1, price = 1.0, name = 'test_data', description = 'test_data_desc'", "id = 1")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 4, price = 1.0, name = 'test_data4', description = 'test_data_desc4'", "id = 4")
        
        database_commands.DataBase().delete_data(self.conn, self.cursor, "products", "id = 999")

        response = self.app.put("/update_product/1/count=2")
        #check if data was updated in the database
        self.cursor.execute("SELECT count FROM products WHERE id = 1")
        row = self.cursor.fetchone()
        #print(response.data)
        self.assertEqual(row[0], 2)
        self.assertEqual(response.data, b"Product updated")
        self.assertEqual(response.status_code, 200)
        
        #before the invalid, test another valid update
        response = self.app.put("/update_product/4/count=3")
        self.cursor.execute("SELECT count FROM products WHERE id = 4")
        row = self.cursor.fetchone()
        self.assertEqual(row[0], 3)
        self.assertEqual(response.data, b"Product updated")
        self.assertEqual(response.status_code, 200)
        
        response = self.app.put("/update_product/999/count=2")
        self.assertEqual(response.data, b"Product not found")
        self.assertEqual(response.status_code, 404)
        
        response = self.app.put("/update_product/invalid_id/count=2")
        self.assertEqual(response.data, b"Invalid id")
        self.assertEqual(response.status_code, 404)
        
        response = self.app.put("/update_product/1/invalid_column=2")
        self.assertEqual(response.data, b"Column invalid_column not found")
        self.assertEqual(response.status_code, 404)
        
        response = self.app.put("/update_product/1/count=invalid_value")
        self.assertEqual(response.data, b"Invalid value")
        self.assertEqual(response.status_code, 404)
        
        response = self.app.put("/update_product/1/count=2&price=1.0&name=test_data&description=test_data_desc")
        self.assertEqual(response.data, b"Product updated")
        self.assertEqual(response.status_code, 200)
        
        response = self.app.put("/update_product/1/count=2&price=1.0&name=test_data&description=test_data_desc&invalid_column=invalid_value")
        self.assertEqual(response.data, b"Column invalid_column not found")
        self.assertEqual(response.status_code, 404)
        
        
    def test_remove_product(self):
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "products", "id, name, price, description, count", (1, "test_data", 1.0, "test_data_desc", 1))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "products", "id, name, price, description, count", (4, "test_data4", 1.0, "test_data_desc4", 4))
        
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 1, price = 1.0, name = 'test_data', description = 'test_data_desc'", "id = 1")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 4, price = 1.0, name = 'test_data4', description = 'test_data_desc4'", "id = 4")
        
        database_commands.DataBase().delete_data(self.conn, self.cursor, "products", "id = 999")
        
        response = self.app.delete("/remove_product/1")
        #check if data was updated in the database
        self.cursor.execute("SELECT count FROM products WHERE id = 1")
        row = self.cursor.fetchone()
        self.assertIsNone(row)
        self.assertEqual(response.data, b"Product removed")
        self.assertEqual(response.status_code, 200)
        
        response = self.app.delete("/remove_product/4")
        self.cursor.execute("SELECT count FROM products WHERE id = 4")
        row = self.cursor.fetchone()
        self.assertIsNone(row)
        self.assertEqual(response.data, b"Product removed")
        self.assertEqual(response.status_code, 200)
        
        response = self.app.delete("/remove_product/999")
        self.assertEqual(response.data, b"Product not found")
        self.assertEqual(response.status_code, 404)
        
        response = self.app.delete("/remove_product/invalid_id")
        self.assertEqual(response.data, b"Invalid id")
        self.assertEqual(response.status_code, 404)
        

    def test_get_image_utility(self):
        database_commands.DataBase().clear_table(self.conn, self.cursor, "images")

        # Create an image using Pillow
        image = Image.new('RGB', (60, 30), color = 'red')
        image.save('images/utility/test_image.png')
        image.close()
        image = Image.new('RGB', (60, 30), color = 'blue')
        image.save('images/utility/test_image2.png')
        image.close()

        try:
            response = self.app.get("/get_image/utility/test_image.png")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'image/png')
            response.close()

        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise    
    #test the following function get_image_product in very detail, and invlid values too
    
    def test_get_image_product(self):
        database_commands.DataBase().clear_table(self.conn, self.cursor, "images")
        database_commands.DataBase().clear_table(self.conn, self.cursor, "products")
        
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "products", "id, name, price, description, count", (1, "test_data", 1.0, "test_data_desc", 1))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "products", "id, name, price, description, count", (4, "test_data4", 1.0, "test_data_desc4", 4))
        
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 1, price = 1.0, name = 'test_data', description = 'test_data_desc'", "id = 1")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 4, price = 1.0, name = 'test_data4', description = 'test_data_desc4'", "id = 4")
        
        database_commands.DataBase().delete_data(self.conn, self.cursor, "products", "id = 999")
        
        #create paths if they don't exist, where the images will be saved
        
        if not os.path.exists("images/products/1"):
            os.makedirs("images/products/1")
            
        if not os.path.exists("images/products/4"):
            os.makedirs("images/products/4")
            
        if not os.path.exists("images/products/999"):
            os.makedirs("images/products/999")
            

        # Create an image using Pillow
        image = Image.new('RGB', (60, 30), color = 'red')
        image.save('images/products/1/1.png')
        image.close()
        image = Image.new('RGB', (60, 30), color = 'blue')
        image.save('images/products/1/2.png')
        image.close()
        image = Image.new('RGB', (60, 30), color = 'red')
        image.save('images/products/4/1.png')
        image.close()
        image = Image.new('RGB', (60, 30), color = 'blue')
        image.save('images/products/4/2.png')
        image.close()
        
        #save the image paths in the database dont use cls
        database_commands.DataBase().insert_data(self.conn, self.cursor, "images", "product_id, image_id, image_path", (1, 1, "images/products/1/1.png"))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "images", "product_id, image_id, image_path", (1, 2, "images/products/1/2.png"))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "images", "product_id, image_id, image_path", (4, 1, "images/products/4/1.png"))
        database_commands.DataBase().insert_data(self.conn, self.cursor, "images", "product_id, image_id, image_path", (4, 2, "images/products/4/2.png"))
        
        
        response = self.app.get("/get_image/1/1")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'image/png')
            response.close()
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        response = self.app.get("/get_image/1/2")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'image/png')
            response.close()
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        response = self.app.get("/get_image/4/1")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'image/png')
            response.close()
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        response = self.app.get("/get_image/4/2")
        #print(response.data)

        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'image/png')
            response.close()
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        response = self.app.get("/get_image/999/1")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, b"Image not found")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        response = self.app.get("/get_image/999/2")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, b"Image not found")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        #test for right exeption if invalid values are passed
        
        response = self.app.get("/get_image/invalid_id/1")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, b"Invalid id")
            
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        response = self.app.get("/get_image/1/invalid_id")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, b"Invalid image id")
            
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
    def test_get_basket_for_user(self):
        database_commands.DataBase().clear_table(self.conn, self.cursor, "baskets")
        database_commands.DataBase().clear_table(self.conn, self.cursor, "products")
        
       
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "products", "id, name, price, description, count", (1, "test_data", 1.0, "test_data_desc", 1))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "products", "id, name, price, description, count", (4, "test_data4", 1.0, "test_data_desc4", 4))
        
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 1, price = 1.0, name = 'test_data', description = 'test_data_desc'", "id = 1")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 4, price = 1.0, name = 'test_data4', description = 'test_data_desc4'", "id = 4")
        
        database_commands.DataBase().delete_data(self.conn, self.cursor, "products", "id = 999")
        
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "baskets", "id, user_id, product_id, count", (1, 1, 1, 1))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "baskets", "id, user_id, product_id, count", (2, 1, 4, 4))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "baskets", "id, user_id, product_id, count", (3, 2, 1, 1))
        
        response = self.app.get("/get_basket_for_user/1")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'{"basket":[{"product":{"count":1,"id":1,"product_id":1,"user_id":1}},{"product":{"count":4,"id":2,"product_id":4,"user_id":1}}]}\n')
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        response = self.app.get("/get_basket_for_user/2")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'{"basket":[{"product":{"count":1,"id":3,"product_id":1,"user_id":2}}]}\n')
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        #invalid values
        response = self.app.get("/get_basket_for_user/invalid_id")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, b"Invalid id")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        response = self.app.get("/get_basket_for_user/999")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, b"User not found")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
    def test_add_product_to_basket(self):
        database_commands.DataBase().clear_table(self.conn, self.cursor, "baskets")
        database_commands.DataBase().clear_table(self.conn, self.cursor, "products")
    
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "products", "id, name, price, description, count", (1, "test_data", 1.0, "test_data_desc", 1))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "products", "id, name, price, description, count", (4, "test_data4", 1.0, "test_data_desc4", 4))
        
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 1, price = 1.0, name = 'test_data', description = 'test_data_desc'", "id = 1")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 4, price = 1.0, name = 'test_data4', description = 'test_data_desc4'", "id = 4")
        
        database_commands.DataBase().delete_data(self.conn, self.cursor, "products", "id = 999")
        
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "baskets", "id, user_id, product_id, count", (1, 1, 1, 1))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "baskets", "id, user_id, product_id, count", (2, 1, 4, 4))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "baskets", "id, user_id, product_id, count", (3, 2, 1, 1))
        
        response = self.app.post("/add_product_to_basket/1/1/1")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b"Product added to basket")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        response = self.app.post("/add_product_to_basket/1/4/4")
        #print(response
        
    def test_remove_product_from_basket(self):
        database_commands.DataBase().clear_table(self.conn, self.cursor, "baskets")
        database_commands.DataBase().clear_table(self.conn, self.cursor, "products")
        database_commands.DataBase().clear_table(self.conn, self.cursor, "sqlite_sequence")
    
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "products", "id, name, price, description, count", (1, "test_data", 1.0, "test_data_desc", 1))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "products", "id, name, price, description, count", (2, "test_data4", 1.0, "test_data_desc4", 4))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "products", "id, name, price, description, count", (4, "test_data4", 1.0, "test_data_desc4", 4))
        
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 1, price = 1.0, name = 'test_data', description = 'test_data_desc'", "id = 1")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 4, price = 1.0, name = 'test_data4', description = 'test_data_desc4'", "id = 4")
        
        database_commands.DataBase().delete_data(self.conn, self.cursor, "products", "id = 999")
        
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "baskets", "id, user_id, product_id, count", (1, 1, 1, 1))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "baskets", "id, user_id, product_id, count", (2, 1, 4, 4))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "baskets", "id, user_id, product_id, count", (3, 2, 1, 1))
        
        response = self.app.delete("/remove_product_from_basket/1/1")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b"Product removed from basket")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        #check if the product was removed from the database
        self.cursor.execute("SELECT * FROM baskets WHERE user_id = 1 AND product_id = 1")
        row = self.cursor.fetchone()
        self.assertIsNone(row)
        
        response = self.app.delete("/remove_product_from_basket/1/4")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b"Product removed from basket")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        response = self.app.delete("/remove_product_from_basket/1/999")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, b"Product not found")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        response = self.app.delete("/remove_product_from_basket/999/1")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, b"User not found")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
    
    def test_clear_basket(self):
        database_commands.DataBase().clear_table(self.conn, self.cursor, "baskets")
        database_commands.DataBase().clear_table(self.conn, self.cursor, "products")
    
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "products", "id, name, price, description, count", (1, "test_data", 1.0, "test_data_desc", 1))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "products", "id, name, price, description, count", (4, "test_data4", 1.0, "test_data_desc4", 4))
        
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 1, price = 1.0, name = 'test_data', description = 'test_data_desc'", "id = 1")
        database_commands.DataBase().update_data(self.conn, self.cursor, "products", "count = 4, price = 1.0, name = 'test_data4', description = 'test_data_desc4'", "id = 4")
        
        database_commands.DataBase().delete_data(self.conn, self.cursor, "products", "id = 999")
        
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "baskets", "id, user_id, product_id, count", (1, 1, 1, 1))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "baskets", "id, user_id, product_id, count", (2, 1, 4, 4))
        database_commands.DataBase().insert_data_at_specific_id(self.conn, self.cursor, "baskets", "id, user_id, product_id, count", (3, 2, 1, 1))
        
        response = self.app.delete("/clear_basket/1")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b"Basket cleared")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        #check if the basket is empty with the database
        self.cursor.execute("SELECT * FROM baskets WHERE user_id = 1")
        row = self.cursor.fetchone()
        self.assertIsNone(row)
        
        response = self.app.delete("/clear_basket/2")
        #print(response.data)

        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b"Basket cleared")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        #check if the basket is empty with the database
        self.cursor.execute("SELECT * FROM baskets WHERE user_id = 2")
        row = self.cursor.fetchone()
        self.assertIsNone(row)
        
        response = self.app.delete("/clear_basket/999")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, b"User not found")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        response = self.app.delete("/clear_basket/invalid_id")
        #print(response.data)
        try:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, b"Invalid id")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        
    def test_get_cookie(self):
        # Old test
        response = self.app.get("/get_cookie")
        try:
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            user_id = data['user_id']
            
            self.cursor.execute("SELECT * FROM cookies WHERE cookie_id = ?", (user_id,))
            row = self.cursor.fetchone()
            self.assertIsNotNone(row)
            
            self.assertEqual(len(user_id), 36)
            self.assertEqual(response.content_type, 'application/json')
            
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        response = self.app.get("/get_cookie")
        try:
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            user_id2 = data['user_id']
            
            self.cursor.execute("SELECT * FROM cookies WHERE cookie_id = ?", (user_id2,))
            row = self.cursor.fetchone()
            self.assertIsNotNone(row)
            
            self.assertEqual(len(user_id2), 36)
            self.assertEqual(response.content_type, 'application/json')
            
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        
        user_id = str(uuid.uuid4())
        
        dataBase.insert_data(self.conn, self.cursor, "cookies", "cookie_id", (user_id,))
        
        response = self.app.get("/get_cookie/" + user_id)
        try:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, b"Cookie already exists")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        # Manually insert a UUID into the database
        user_id = str(uuid.uuid4())

        # First request to the endpoint should be successful
        response = self.app.get(f"/get_cookie/{user_id}")
        self.assertEqual(response.status_code, 200)
        
        user_id = str(uuid.uuid4())

        # Second request to the endpoint with the same UUID should return 404
        response = self.app.get(f"/get_cookie/{user_id}")
        self.assertEqual(response.status_code, 200)
        
        # Manually insert a UUID into the database
        user_id = str(uuid.uuid4())

        # First request to the endpoint should be successful
        response = self.app.get(f"/get_cookie/{user_id}")
        self.assertEqual(response.status_code, 200)

        # Second request to the endpoint with the same UUID should return 404
        response = self.app.get(f"/get_cookie/{user_id}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_data(as_text=True), "Cookie already exists")
        
    def test_check_cookie(self):
        response = self.app.get("/get_cookie")
        try:
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            user_id = data['user_id']
            
            self.cursor.execute("SELECT * FROM cookies WHERE cookie_id = ?", (user_id,))
            row = self.cursor.fetchone()
            self.assertIsNotNone(row)
            
            self.assertEqual(len(user_id), 36)
            self.assertEqual(response.content_type, 'application/json')
            
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        response = self.app.get("/check_cookie/" + user_id)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b"Cookie found")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
        
        response = self.app.get("/check_cookie/invalid_id")
        try:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data, b"Cookie not found")
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
            raise
    
    
    def tearDown(self):
        self.app = None
        
if __name__ == "__main__":
    unittest.main()