import sqlite3

class DataBase():
    def connect_database(name):
        if name[-3:] != ".db":
            name = name + ".db"
            
        connection = sqlite3.connect(name)
        cursor = connection.cursor()
        
        return cursor, connection
    
    def disconnect_database(connection):
        connection.commit()
        connection.close()
        
    def create_table(cursor, connection, name, columns):
        cursor.execute("CREATE TABLE IF NOT EXISTS " + name + " (" + columns + ")")
        connection.commit()
        
    def insert_data(cursor, connection, table, columns, data):
        cursor.execute("INSERT INTO " + table + " (" + columns + ") VALUES (" + data + ")")
        connection.commit()
        
    def select_data(cursor, table, columns, condition):
        cursor.execute("SELECT " + columns + " FROM " + table + " WHERE " + condition)
        return cursor.fetchall()
    
    def update_data(cursor, connection, table, columns, condition):
        cursor.execute("UPDATE " + table + " SET " + columns + " WHERE " + condition)
        connection.commit()
        
    def delete_data(cursor, connection, table, condition):
        cursor.execute("DELETE FROM " + table + " WHERE " + condition)
        connection.commit()
        
    def drop_table(cursor, connection, table):
        cursor.execute("DROP TABLE " + table)
        connection.commit()