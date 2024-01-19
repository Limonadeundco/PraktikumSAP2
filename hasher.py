import bcrypt
import database_commands.database_commands as database_commands

DataBase = database_commands.DataBase()

connection, cursor = DataBase.connect_database("users.db")
DataBase.create_table(connection, cursor, "users", "username, password")

username = "admin"
password = "root"
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Now you can store hashed_password in the database
DataBase.insert_data(connection, cursor, "users", "username, password", (username, hashed_password))   