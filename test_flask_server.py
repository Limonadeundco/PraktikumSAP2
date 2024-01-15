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
        try:
            self.assertEqual(response.data, b"[('test_data',)]")
        except AssertionError:
            print("Unexpected response data:", response.data)
            raise
        self.assertEqual(response.status_code, 200)
        
        
    
    def tearDown(self):
        self.app = None
        
if __name__ == "__main__":
    unittest.main()