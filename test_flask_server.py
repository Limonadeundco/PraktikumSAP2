import unittest
import flask_server
import flask
import database_commands

class TestFlaskServer(unittest.TestCase):
    def setUp(self):
        self.app = flask_server.app.test_client()
        self.Server = flask_server.Server()
        self.app.testing = True
        self.conn, self.cursor = database_commands.DataBase().connect_database("database.db")

    
    def test_insert_data(self):
        response = self.app.post("/update_product/1/count/-1")
        self.assertEqual(response.data, b"Data inserted")
    
    def test_get_data(self):
        response = self.app.get("/get_product/1/count")
        self.assertEqual(response.data, b"[('test_data',)]")
        self.assertEqual(response.status_code, 200)
        response = self.app.get("/get_product/999/count")
        self.assertEqual(response.data, b"[]")
        self.assertEqual(response.status_code, 199)
        
        response = self.app.get("/get_product/1/price")
        self.assertEqual(response.data, b"[('test_data',)]")
        self.assertEqual(response.status_code, 200)
        
        response = self.app.get("/get_product/1/name")
        self.assertEqual(response.data, b"[('test_data',)]")
        self.assertEqual(response.status_code, 200)
        
        
    
    def tearDown(self):
        self.app = None
        
if __name__ == "__main__":
    unittest.main()