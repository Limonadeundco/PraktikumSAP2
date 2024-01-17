import unittest
from recommended_product_functions import *
import os
import sqlite3
import database_commands.database_commands as database_commands
from datetime import datetime

current_year = datetime.now().year
current_month = datetime.now().month
current_day = datetime.now().day


class TestRecommendedProductFunctions(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.recommended_product_functions = recommended_product_functions()
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.dataBase = database_commands.DataBase()
        
        self.dataBase.drop_table(self.connection, self.cursor, "products")
        self.dataBase.drop_table(self.connection, self.cursor, "sales")
        self.dataBase.drop_table(self.connection, self.cursor, "recommended_products")
        
        self.dataBase.create_table(self.connection, self.cursor, "products", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, description TEXT, count INTEGER, sales INTEGER")
        
        self.dataBase.create_table(self.connection, self.cursor, "sales", "id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, sale_time TEXT, count INTEGER")
        
        self.dataBase.create_table(self.connection, self.cursor, "recommended_products", "id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, sales_last_day INTEGER")
        
    @classmethod
    def tearDownClass(self):
        self.connection.close()
        
    
    def setUp(self):
        #clear tables
        self.dataBase.clear_table(self.connection, self.cursor, "products")
        self.dataBase.clear_table(self.connection, self.cursor, "sales")
        self.dataBase.clear_table(self.connection, self.cursor, "recommended_products")
        
        #generate test data
        self.dataBase.insert_data(self.connection, self.cursor, "products", "name, price, description, count, sales", ("product1", 1.0, "description1", 1, 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "products", "name, price, description, count, sales", ("product2", 1.0, "description2", 1, 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "products", "name, price, description, count, sales", ("product3", 1.0, "description3", 1, 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "products", "name, price, description, count, sales", ("product4", 1.0, "description4", 1, 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "products", "name, price, description, count, sales", ("product5", 1.0, "description5", 1, 1,))

        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (1, f"{current_year}-{current_month}-{current_day} 00:10:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (1, f"{current_year}-{current_month}-{current_day} 00:30:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (1, f"{current_year}-{current_month}-{current_day} 00:50:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (1, f"{current_year}-{current_month}-{current_day} 00:00:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (2, f"{current_year}-{current_month}-{current_day} 00:20:00", 1,))

        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (2, f"{current_year}-{current_month}-{current_day} 00:30:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (2, f"{current_year}-{current_month}-{current_day} 00:50:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (2, f"{current_year}-{current_month}-{current_day} 00:40:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (3, f"{current_year}-{current_month}-{current_day} 00:00:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (3, f"{current_year}-{current_month}-{current_day} 00:20:00", 1,))

        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (3, f"{current_year}-{current_month}-{current_day} 00:10:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (4, f"{current_year}-{current_month}-{current_day} 00:40:00", 1,))
        self.dataBase.insert_data(self.connection, self.cursor, "sales", "product_id, sale_time, count", (4, f"{current_year}-{current_month}-{current_day} 00:30:00", 1,))
        
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
        
        # check if the generate_recommended_products throws an error if the product_count is bigger than the number of products
        with self.assertRaises(IndexError):
            self.recommended_product_functions.generate_recommended_products(self.connection, self.cursor, 6)
            
        # check if the generate_recommended_products throws an error if the product_count is smaller than 1
        with self.assertRaises(IndexError):
            self.recommended_product_functions.generate_recommended_products(self.connection, self.cursor, 0)
            
        # check if the generate_recommended_products throws an error if the product_count is not an integer
        with self.assertRaises(TypeError):
            self.recommended_product_functions.generate_recommended_products(self.connection, self.cursor, "test")
        

        
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