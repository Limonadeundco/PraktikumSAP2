import datetime

class recommended_product_functions():
    def __init__(self):
        pass
    
    def generate_recommended_products(self, connection, cursor, product_count):
        cursor.execute("SELECT id FROM products")
        dataBase_response = cursor.fetchall()
        
        products_sales = []
        for product_id in dataBase_response:
            sales_last_day = self.get_sales_last_day(connection, cursor, product_id)
            products_sales.append([product_id, sales_last_day])
            
        products_sales.sort(key=lambda x: x[1], reverse=True)
        
        for i in range(product_count):
            product_id = products_sales[i][0]
            product_sales = products_sales[i][1]
            self.insert_data(connection, cursor, "recommended_products", "product_id, sales_last_day", (product_id, product_sales,))
            
        
    def get_sales_last_day(self, connection, cursor, product_id):
        # Get current time
        current_time = datetime.datetime.now()

        # Calculate the time 24 hours ago
        last_day_time = current_time - datetime.timedelta(days=1)

        # Execute SQL query to get sales from the last 24 hours
        cursor.execute(f"SELECT id FROM sales WHERE sale_time >= {last_day_time} AND product_id = {product_id}")
        dataBase_response = cursor.fetchall()
        
        sales_last_day = len(dataBase_response)
        
        return sales_last_day