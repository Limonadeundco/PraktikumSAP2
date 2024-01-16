import datetime
import database_commands.database_commands as database_commands

class recommended_product_functions():
    def __init__(self):
        self.dataBase = database_commands.DataBase()
    
    def generate_recommended_products(self, connection, cursor, product_count):
        cursor.execute("SELECT id FROM products")
        dataBase_response = cursor.fetchall()
        
        if product_count == 0:
            raise IndexError("The product_count must be bigger than 0")
        #if it is not an integer, raise TypeError
        if type(product_count) != int:
            raise TypeError("The product_count must be an integer")
        
        products_sales = []
        for product_id in dataBase_response:
            sales_last_day = self.get_sales_last_day(connection, cursor, product_id[0])
            #print("sales_last_day: ", sales_last_day)
            products_sales.append([product_id[0], sales_last_day])
            
        products_sales.sort(key=lambda x: x[1], reverse=True)
        
        for i in range(product_count):
            #print("products_sales[i]: ", products_sales[i])
            product_id = products_sales[i][0]
            product_sales = products_sales[i][1]
            #print("product_id: ", product_id, "product_sales: ", product_sales)
            self.dataBase.insert_data(connection, cursor, "recommended_products", "product_id, sales_last_day", (product_id, product_sales,))
            
        
    def get_sales_last_day(self, connection, cursor, product_id):
        # Get current time
        current_time = datetime.datetime.now()

        # Calculate the time 24 hours ago
        last_day_time = current_time - datetime.timedelta(days=1)

        # Format the last_day_time to a string
        last_day_time_str = last_day_time.strftime('%Y-%m-%d %H:%M:%S')

        # Execute SQL query to get sales from the last 24 hours
        cursor.execute(f"SELECT id FROM sales WHERE sale_time >= '{last_day_time_str}' AND product_id = '{product_id}'")
        dataBase_response = cursor.fetchall()
        #print("dataBase_response: ", dataBase_response)

        sales_last_day = len(dataBase_response)
        #print("sales_last_day: ", sales_last_day)

        return sales_last_day