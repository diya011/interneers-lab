import unittest
from unittest.mock import patch
from product.service.prod_service import ProductService
from product.service.prod_category_service import ProductCategoryService


class TestProductService(unittest.TestCase):

    @patch('product.service.prod_service.ProductRepository.create_product')
    def test_create_product(self, mock_create):
        mock_create.return_value = {'name': 'Test', 'price': 100}
        data = {'name': 'Test', 'price': 100}
        result = ProductService.create_product(data)
        self.assertEqual(result['name'], 'Test')
        mock_create.assert_called_once_with(data)

    @patch('product.service.prod_service.ProductRepository.get_product_by_id')
    def test_get_product(self, mock_get):
        mock_get.return_value = {'id': '123', 'name': 'Sample'}
        result = ProductService.get_product('123')
        self.assertEqual(result['id'], '123')
        mock_get.assert_called_once_with('123')

    @patch('product.service.prod_service.ProductRepository.get_all_products')
    def test_get_all_products(self, mock_get_all):
        mock_get_all.return_value = [{'id': '1'}, {'id': '2'}]
        result = ProductService.get_all_products()
        self.assertEqual(len(result), 2)
        mock_get_all.assert_called_once()

    @patch('product.service.prod_service.ProductRepository.update_product')
    def test_update_product(self, mock_update):
        mock_update.return_value = {'name': 'Updated'}
        result = ProductService.update_product('1', {'name': 'Updated'})
        self.assertEqual(result['name'], 'Updated')
        mock_update.assert_called_once_with('1', {'name': 'Updated'})

    @patch('product.service.prod_service.ProductRepository.delete_product')
    def test_delete_product(self, mock_delete):
        mock_delete.return_value = True
        result = ProductService.delete_product('1')
        self.assertTrue(result)
        mock_delete.assert_called_once_with('1')

    @patch('product.service.prod_service.ProductRepository.get_by_category')
    def test_get_products_by_category(self, mock_get_by_cat):
        mock_get_by_cat.return_value = [{'id': '1'}]
        result = ProductService.get_products_by_category('cat1')
        self.assertEqual(result[0]['id'], '1')
        mock_get_by_cat.assert_called_once_with('cat1')

    @patch('product.service.prod_service.ProductRepository.set_category')
    def test_add_product_to_category(self, mock_set_cat):
        mock_set_cat.return_value = True
        result = ProductService.add_product_to_category('p1', 'c1')
        self.assertTrue(result)
        mock_set_cat.assert_called_once_with('p1', 'c1')

    @patch('product.service.prod_service.ProductRepository.remove_category')
    def test_remove_product_from_category(self, mock_remove_cat):
        mock_remove_cat.return_value = True
        result = ProductService.remove_product_from_category('p1', 'c1')
        self.assertTrue(result)
        mock_remove_cat.assert_called_once_with('p1', 'c1')
