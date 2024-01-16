import unittest
from recommended_product_functions import *
import os
import sqlite3
import database_commands.database_commands as database_commands


class TestRecommendedProductFunctions(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.recommended_product_functions = recommended_product_functions()
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.dataBase = database_commands.DataBase()
        
        self.dataBase.create_table(self.connection, self.cursor, "products", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, description TEXT, count INTEGER, sales INTEGER")
        
        self.dataBase.create_table(self.connection, self.cursor, "sales", "id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, sale_time TEXT, count INTEGER")
        
        self.dataBase.create_table(self.connection, self.cursor, "recommended_products", "id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, sales_last_day INTEGER")
        
    @classmethod
    def tearDownClass(self):
        self.connection.close()
        os.remove("TestRecommendedProductFunctions.db")
        
    
    def setUp(self):
        #clear tables
        self.dataBase.clear_table(self.connection, self.cursor, "products")
        self.dataBase.clear_table(self.connection, self.cursor, "sales")
        self.dataBase.clear_table(self.connection, self.cursor, "recommended_products")
        
        #generate test data
        self.dataBase.insert_data(self.connection, self.cursor, "products", "name, price, description, count, sales", ("test_product_1", 100, "test_description_1", 10, 0,))
        self.dataBase.insert_data(self.connection, self.cursor, "products", "name, price, description, count, sales", ("test_product_2", 200, "test_description_2", 20, 0,))
        self.dataBase.insert_data(self.connection, self.cursor, "products", "name, price, description, count, sales", ("test_product_3", 300, "test_description_3", 30, 0,))
        self.dataBase.insert_data(self.connection, self.cursor, "products", "name, price, description, count, sales", ("test_product_4", 400, "test_description_4", 40, 0,))
        self.dataBase.insert_data(self.connection, self.cursor, "products", "name, price, description, count, sales", ("test_product_5", 500, "test_description_5", 50, 0,))
        
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (1, "2024-01-15 00:10:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (1, "2024-01-15 00:30:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (1, "2024-01-15 00:50:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (1, "2024-01-15 00:00:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (2, "2024-01-15 00:20:00", 1,))
        
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (2, "2024-01-15 00:30:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (2, "2024-01-15 00:50:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (2, "2024-01-15 00:40:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (3, "2024-01-15 00:00:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (3, "2024-01-15 00:20:00", 1,))
        
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (3, "2024-01-15 00:10:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (4, "2024-01-15 00:40:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (4, "2024-01-15 00:30:00", 1,))
        
    def test_generate_recommended_products(self):
        self.recommended_product_functions.generate_recommended_products(self.connection, self.cursor, 5)
        
        self.cursor.execute("SELECT * FROM recommended_products")
        dataBase_response = self.cursor.fetchall()
        
        self.assertEqual(dataBase_response[0][1], 1)
        self.assertEqual(dataBase_response[1][1], 2)
        self.assertEqual(dataBase_response[2][1], 3)
        self.assertEqual(dataBase_response[3][1], 4)
        self.assertEqual(dataBase_response[4][1], 5)
        
        #test if the sales_last_day is correct
        self.cursor.execute("SELECT * FROM recommended_products WHERE product_id = 1")
        dataBase_response = self.cursor.fetchall()
        self.assertEqual(dataBase_response[0][2], 4)
        self.cursor.execute("SELECT * FROM recommended_products WHERE product_id = 2")
        dataBase_response = self.cursor.fetchall()
        self.assertEqual(dataBase_response[0][2], 4)
        self.cursor.execute("SELECT * FROM recommended_products WHERE product_id = 3")
        dataBase_response = self.cursor.fetchall()
        self.assertEqual(dataBase_response[0][2], 3)
        
        #check if the id is unigue
        self.cursor.execute("SELECT * FROM recommended_products")
        dataBase_response = self.cursor.fetchall()
        self.assertEqual(dataBase_response[0][0], 1)
        self.assertEqual(dataBase_response[1][0], 2)
        self.assertEqual(dataBase_response[2][0], 3)
        self.assertEqual(dataBase_response[3][0], 4)
        
        #print(dataBase_response)
        

        
    def test_get_sales_last_day(self):
        sales_last_day = self.recommended_product_functions.get_sales_last_day(self.connection, self.cursor, 1)
        self.assertEqual(sales_last_day, 4)
        
        sales_last_day = self.recommended_product_functions.get_sales_last_day(self.connection, self.cursor, 2)
        self.assertEqual(sales_last_day, 4)
        
        sales_last_day = self.recommended_product_functions.get_sales_last_day(self.connection, self.cursor, 3)
        self.assertEqual(sales_last_day, 3)
        
        sales_last_day = self.recommended_product_functions.get_sales_last_day(self.connection, self.cursor, 4)
        self.assertEqual(sales_last_day, 2)
        
        sales_last_day = self.recommended_product_functions.get_sales_last_day(self.connection, self.cursor, 5)
        self.assertEqual(sales_last_day, 0)
        
        
if __name__ == '__main__':
    unittest.main()