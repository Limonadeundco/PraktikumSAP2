import unittest

# Import the test modules
from database_commands.test_database_commands import TestDatabaseCommands
from test_flask_server import TestFlaskServer
from test_recommended_product_functions import TestRecommendedProductFunctions

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()

    # Create a test loader
    loader = unittest.TestLoader()

    # Add the test cases to the suite
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseCommands))
    suite.addTests(loader.loadTestsFromTestCase(TestFlaskServer))
    suite.addTests(loader.loadTestsFromTestCase(TestRecommendedProductFunctions))

    # Create a test runner
    runner = unittest.TextTestRunner()

    # Run the tests
    runner.run(suite)