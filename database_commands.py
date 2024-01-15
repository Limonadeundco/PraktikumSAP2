import sqlite3

class DataBase():
    def connect_database(self, name):
        if name[-3:] != ".db":
            name = name + ".db"
            
        connection = sqlite3.connect(name)
        cursor = connection.cursor()
        
        return connection, cursor
    
    def disconnect_database(self, connection):
        connection.close()
        return None
        
    def create_table(self, connection, cursor, name, columns):
        cursor.execute("CREATE TABLE IF NOT EXISTS " + name + " (" + columns + ")")
        connection.commit()
            
    def insert_data(self, connection, cursor, table, columns, data):
        placeholders = ', '.join('?' for item in data)
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, data)
        connection.commit()
        
    def insert_data_at_specific_id(self, connection, cursor, table, columns, data, id):
        placeholders1 = ', '.join('?' for item in data)
        placeholders2 = ', '.join('?' for item in columns.split(", "))
        query = f"UPDATE {table} SET {placeholders1} = {placeholders2} WHERE id={id}"
        cursor.execute(query, columns, data)
        connection.commit()
        
    def select_data(self, cursor, table, columns, condition):
        cursor.execute("SELECT " + columns + " FROM " + table + " WHERE " + condition)
        return cursor.fetchall()
    
    def update_data(self, connection, cursor, table, columns, condition):
        cursor.execute("UPDATE " + table + " SET " + columns + " WHERE " + condition)
        connection.commit()
        
    def delete_data(self, connection, cursor, table, condition):
        cursor.execute("DELETE FROM " + table + " WHERE " + condition)
        connection.commit()
        
    def drop_table(self, conn, cursor, table):
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
        if cursor.fetchone():
            cursor.execute("DROP TABLE " + table)
        conn.commit()