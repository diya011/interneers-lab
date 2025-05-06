import unittest
from product.views import validate_product_data, validate_category_data

class TestValidationFunctions(unittest.TestCase):

    def test_validate_product_data_valid(self):
        data = {
            "name": "Laptop",
            "price": 1000.0,
            "brand": "Dell",
            "quantity": 5
        }
        self.assertIsNone(validate_product_data(data))

    def test_validate_product_data_missing_field(self):
        data = {
            "name": "Laptop",
            "price": 1000.0,
            "brand": "Dell"
        }
        self.assertEqual(validate_product_data(data), "quantity is required")

    def test_validate_product_data_invalid_price(self):
        data = {
            "name": "Laptop",
            "price": -10,
            "brand": "Dell",
            "quantity": 5
        }
        self.assertEqual(validate_product_data(data), "Price must be a non-negative number")

    def test_validate_product_data_invalid_quantity(self):
        data = {
            "name": "Laptop",
            "price": 1000,
            "brand": "Dell",
            "quantity": -3
        }
        self.assertEqual(validate_product_data(data), "Quantity must be a non-negative integer")

    def test_validate_category_data_valid(self):
        self.assertIsNone(validate_category_data({"title": "Kitchen"}))

    def test_validate_category_data_blank_title(self):
        self.assertEqual(validate_category_data({"title": "  "}), "Title is required")

    def test_validate_category_data_missing_title(self):
        self.assertEqual(validate_category_data({}), "Title is required")
