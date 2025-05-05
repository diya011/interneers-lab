import pytest
import json
from django.test import Client
from seed_data.seed_product_category import seed_product_categories
from seed_data.seed_product import seed_products

import django
django.setup()

client = Client()

@pytest.mark.django_db
class TestProductIntegration:

    def test_create_product(self):
        categories = seed_product_categories()
        payload = {
            "name": "Milk",
            "description": "Fresh milk",
            "price": 30.0,
            "category_id": str(categories[0].id),
            "brand": "DairyCo",
            "quantity": 2
        }
        response = client.post("/product/create/", json.dumps(payload), content_type="application/json")
        assert "id" in response.json()
        assert response.json()["message"] == "Product created"

    def test_get_all_products(self):
        categories = seed_product_categories()
        seed_products(categories[0].id)
        response = client.get("/product/list/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2

    def test_get_product_by_id(self):
        categories = seed_product_categories()
        products = seed_products(categories[0].id)
        product = products[0]
        response = client.get(f"/product/{str(product.id)}/")
        assert response.status_code == 200
        assert response.json()["name"] == "Bread"

    def test_update_product(self):
        categories = seed_product_categories()
        products = seed_products(categories[0].id)
        product = products[0]
        payload = {
            "name": "Updated Bread",
            "description": "Fresh and crispy",
            "price": 55.0,
            "category_id": str(categories[0].id),
            "brand": "harvest",
            "quantity": 5
        }
        response = client.put(f"/product/update/{str(product.id)}/", json.dumps(payload), content_type="application/json")
        print(response.json())
        assert response.status_code == 200
        assert response.json()["message"] == "Product updated"


    def test_delete_product(self):
        categories = seed_product_categories()
        products = seed_products(categories[0].id)
        product = products[0]
        response = client.delete(f"/product/delete/{str(product.id)}/")
        assert response.json()["message"] == "Product deleted"


    def test_get_products_by_category(self):
        categories = seed_product_categories()
        seed_products(categories[0].id)
        response = client.get(f"/product/get_category/{str(categories[0].id)}/")
        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        assert len(products) >= 1  # Ensure at least one product is listed

    def test_add_product_to_category(self):
        categories = seed_product_categories()
        products = seed_products(categories[0].id)
        product = products[0]
        new_category = seed_product_categories()[1]  # Assuming there's a second category for this test

        response = client.put(f"/product/{str(product.id)}/add_to_category/{str(new_category.id)}/")
        assert response.status_code == 200
        assert response.json()["message"] == "Product added to category successfully"

    def test_remove_product_from_category(self):
        categories = seed_product_categories()
        products = seed_products(categories[0].id)
        product = products[0]

        print(f"Testing removal for product {product.id} from category {categories[0].id}")
        response = client.put(f"/product/{str(product.id)}/remove_from_category/")   
        
        print(response.json()) 
        
        assert response.status_code == 200
        assert response.json()["message"] == "Product removed from category successfully"

    def test_create_category(self):
        payload = {
            "title": "Electronics",
            "description": "Gadgets and appliances"
        }
        response = client.post("/product/category/create/", json.dumps(payload), content_type="application/json")
        assert response.status_code == 201
        assert "id" in response.json()
        assert response.json()["message"] == "Category created"

    def test_get_all_categories(self):
        seed_product_categories()
        response = client.get("/product/category/all/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # Ensure at least one category exists

    def test_get_category_by_id(self):
        categories = seed_product_categories()
        category = categories[0]
        response = client.get(f"/product/category/get/{str(category.id)}/")
        assert response.status_code == 200
        assert response.json()["title"] == category.title

    def test_update_category(self):
        categories = seed_product_categories()
        category = categories[0]
        payload = {
            "title": "Updated Electronics",
            "description": "Updated gadgets and appliances"
        }
        response = client.put(f"/product/category/update/{str(category.id)}/", json.dumps(payload), content_type="application/json")
        assert response.status_code == 200
        assert response.json()["message"] == "Category updated"

    def test_delete_category(self):
        categories = seed_product_categories()
        category = categories[0]
        response = client.delete(f"/product/category/delete/{str(category.id)}/")
        assert response.json()["message"] == "Category deleted"