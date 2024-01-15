import sqlite3

class DataBase():
    def connect_database(self, name):
        if name[-3:] != ".db":
            name = name + ".db"
            
        connection = sqlite3.connect(name)
        cursor = connection.cursor()
        
        return cursor, connection
    
    def disconnect_database(self, connection):
        connection.close()
        return None
        
    def create_table(self, cursor, connection, name, columns):
        cursor.execute("CREATE TABLE IF NOT EXISTS " + name + " (" + columns + ")")
        connection.commit()
            
    def insert_data(self, cursor, connection, table, columns, data):
        placeholders = ', '.join('?' for item in data)
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, data)
        connection.commit()
        
    def select_data(self, cursor, table, columns, condition):
        cursor.execute("SELECT " + columns + " FROM " + table + " WHERE " + condition)
        return cursor.fetchall()
    
    def update_data(self, cursor, connection, table, columns, condition):
        cursor.execute("UPDATE " + table + " SET " + columns + " WHERE " + condition)
        connection.commit()
        
    def delete_data(self, cursor, connection, table, condition):
        cursor.execute("DELETE FROM " + table + " WHERE " + condition)
        connection.commit()
        
    def drop_table(self, cursor, connection, table):
        cursor.execute("DROP TABLE " + table)
        connection.commit()