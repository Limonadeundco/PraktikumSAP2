import unittest
import flask_server
import flask
import database_commands

class TestFlaskServer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        #delete database and reset everything
        cls.conn, cls.cursor = database_commands.DataBase().connect_database("database.db")
        database_commands.DataBase().drop_table(cls.conn, cls.cursor, "products")
        database_commands.DataBase().create_table(cls.conn, cls.cursor, "products", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, description TEXT, count INTEGER")
        
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

    
    def test_insert_data(self):
        response = self.app.post("/add_product/name=TestProduct&price=1.0&description=TestDescription&count=1")
        self.assertEqual(response.data, b"Product added")

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
        # recommended products are products with the highest count
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
        
        response = self.app.get("/recommended_products/3")
        
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
        print(response.data)
        try:
            self.assertEqual(response.data, expected_data)
        except AssertionError:
            self.fail("Unexpected response data:" + str(response.data))
        self.assertEqual(response.status_code, 200)
        
        
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
        print(response.data)
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
        self.assertEqual(response.data, b"Column not found")
        self.assertEqual(response.status_code, 404)
        
        response = self.app.put("/update_product/1/count=invalid_value")
        self.assertEqual(response.data, b"Invalid value")
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
        
    #def test_
        
    
    def tearDown(self):
        self.app = None
        
if __name__ == "__main__":
    unittest.main()