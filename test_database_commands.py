import unittest
import database_commands
import sqlite3


class TestDatabaseCommands(unittest.TestCase):
    def setUp(self):
        self.DataBase = database_commands.DataBase()
        
    
    def tearDown(self):
        self.DataBase = None
    
    def test_connect_database(self):
        connection, cursor = self.DataBase.connect_database("test")
        self.assertIsInstance(cursor, sqlite3.Cursor)
        self.assertIsInstance(connection, sqlite3.Connection)

        connection, cursor = self.DataBase.connect_database("test.db")
        self.assertIsInstance(cursor, sqlite3.Cursor)
        self.assertIsInstance(connection, sqlite3.Connection)
    
    def test_disconnect_database(self):
        connection = sqlite3.connect("test.db")
        connection = self.DataBase.disconnect_database(connection)
        self.assertIsNone(connection, "Connection was not closed")
        
    def test_create_table(self):
        connection, cursor = self.DataBase.connect_database("test")
        self.DataBase.create_table(connection, cursor, "test", "test")
        try:
            cursor.execute("SELECT * FROM test")
            cursor.fetchone()
        except sqlite3.OperationalError:
            self.fail("Table 'test' was not created")
        self.DataBase.drop_table(connection, cursor, "test")
        self.DataBase.disconnect_database(connection)
        
    def test_insert_data(self):
        connection, cursor = self.DataBase.connect_database("test")
        self.DataBase.create_table(connection, cursor, "test", "test")
        self.DataBase.insert_data(connection, cursor, "test", "test", ("test",))
        cursor.execute("SELECT * FROM test")
        row = cursor.fetchone()
        self.assertIsNotNone(row, "No data was inserted")
        self.DataBase.drop_table(connection, cursor, "test")
        self.DataBase.disconnect_database(connection)
        
    def test_insert_data_at_specific_id(self):
        connection, cursor = self.DataBase.connect_database("test")
        self.DataBase.create_table(connection, cursor, "test", "test")
        self.DataBase.insert_data_at_specific_id(connection, cursor, "test", "test", ("test",), 1)
        cursor.execute("SELECT * FROM test")
        row = cursor.fetchone()
        self.assertIsNotNone(row, "No data was inserted")
        
        #again but with a different id
        self.DataBase.insert_data_at_specific_id(connection, cursor, "test", "test", ("test",), 2)
        cursor.execute("SELECT * FROM test WHERE id=2")
        row = cursor.fetchone()
        self.assertIsNotNone(row, "No data was inserted")
        
        #again but with a different id
        self.DataBase.insert_data_at_specific_id(connection, cursor, "test", "test", ("test",), 3)
        cursor.execute("SELECT * FROM test WHERE id=3")
        row = cursor.fetchone()
        self.assertIsNotNone(row, "No data was inserted")

        self.DataBase.insert_data_at_specific_id(connection, cursor, "", "", ("",), 4)
        cursor.execute("SELECT * FROM test WHERE id=4")
        row = cursor.fetchone()
        self.assertIsNotNone(row, "No data was inserted")

        self.DataBase.drop_table(connection, cursor, "test")
        self.DataBase.disconnect_database(connection)
        
        
        
    def test_select_data(self):
        connection, cursor = self.DataBase.connect_database("test")
        self.DataBase.create_table(connection, cursor, "test", "test")
        self.DataBase.insert_data(connection, cursor, "test", "test", ("test",))
        cursor.execute("SELECT * FROM test")
        row = cursor.fetchone()
        self.assertIsNotNone(row, "No data was found")
        self.DataBase.drop_table(connection, cursor, "test")
        self.DataBase.disconnect_database(connection)
        
    def test_update_data(self):
        connection, cursor = self.DataBase.connect_database("test")
        self.DataBase.create_table(connection, cursor, "test", "test")
        self.DataBase.insert_data(connection, cursor, "test", "test", ("test",))
        self.DataBase.update_data(connection, cursor, "test", "test='updated'", "test='test'")
        cursor.execute("SELECT * FROM test WHERE test='updated'")
        row = cursor.fetchone()
        self.assertIsNotNone(row, "Data was not updated")
        self.DataBase.drop_table(connection, cursor, "test")
        self.DataBase.disconnect_database(connection)
        
    def test_delete_data(self):
        connection, cursor = self.DataBase.connect_database("test")
        self.DataBase.create_table(connection, cursor, "test", "test")
        self.DataBase.insert_data(connection, cursor, "test", "test", ("test",))
        self.DataBase.delete_data(connection, cursor, "test", "test='test'")
        cursor.execute("SELECT * FROM test WHERE test='test'")
        row = cursor.fetchone()
        self.assertIsNone(row, "Data was not deleted")
        self.DataBase.drop_table(connection, cursor, "test")
        self.DataBase.disconnect_database(connection)
        
    def test_drop_table(self):
        connection, cursor = self.DataBase.connect_database("test")
        self.DataBase.create_table(connection, cursor, "test", "test")
        self.DataBase.insert_data(connection, cursor, "test", "test", ("test",))
        self.DataBase.drop_table(connection, cursor, "test")
        try:
            cursor.execute("SELECT * FROM test")
            cursor.fetchone()
            self.fail("Table 'test' was not dropped")
        except sqlite3.OperationalError:
            pass
        self.DataBase.disconnect_database(connection)
        
        #drop a table that does not exist
        connection, cursor = self.DataBase.connect_database("test")
        self.DataBase.drop_table(connection, cursor, "test")
        self.DataBase.disconnect_database(connection)
        
        
        
    
    
    
        
if __name__ == '__main__':
    unittest.main()