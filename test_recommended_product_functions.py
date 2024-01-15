import unittest
from recommended_product_functions import *
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import Mock

class TestRecommendedProductFunctions(unittest.TestCase):
    
    def setUp(self):
        self.recommended_product_functions = recommended_product_functions()
        self.connection = Mock()
        self.cursor = Mock()
        
    def test_generate_recommended_products(self):
        self.cursor.fetchall.return_value = [[1], [2], [3]]
        self.recommended_product_functions.get_sales_last_day = MagicMock(return_value=1)
        self.recommended_product_functions.insert_data = MagicMock()
        
        self.recommended_product_functions.generate_recommended_products(self.connection, self.cursor, 3)
        
        self.recommended_product_functions.get_sales_last_day.assert_called()
        self.recommended_product_functions.insert_data.assert_called()
        
    def test_get_sales_last_day(self):
        self.cursor.fetchall.return_value = [[1], [2], [3]]
        
        self.recommended_product_functions.get_sales_last_day(self.connection, self.cursor, 1)
        
        self.cursor.execute.assert_called()
        
        
if __name__ == '__main__':
    unittest.main()