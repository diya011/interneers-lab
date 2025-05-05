import json
import pytest
from django.test import Client
from product.tests.seed_data.seed_product_category import seed_product_categories

client = Client()

@pytest.mark.django_db
class TestProductCategoryIntegration:

    def test_create_product_category(self):
        payload = {
            "title": "Electronics",
            "description": "Electronic devices"
        }
        response = client.post("/product/category/create/", json.dumps(payload), content_type="application/json")
        assert response.status_code == 201
        assert response.json()["message"] == "Category created"

    def test_get_all_product_categories(self):
        seed_product_categories()
        response = client.get("/product/category/all/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2

    def test_get_product_category_by_id(self):
        categories = seed_product_categories()
        category = categories[0]
        response = client.get(f"/product/category/get/{str(category.id)}/")
        assert response.status_code == 200
        assert response.json()["title"] == "Food"

    def test_update_product_category(self):
        categories = seed_product_categories()
        category = categories[0]
        payload = {
            "title": "Updated Food",
            "description": "Updated description"
        }
        response = client.put(f"/product/category/update/{str(category.id)}/", json.dumps(payload), content_type="application/json")
        print(response.json())
        assert response.status_code == 200
        assert response.json()["message"] == "Category updated"

    def test_delete_product_category(self):
        categories = seed_product_categories()
        category = categories[0]
        response = client.delete(f"/product/category/delete/{str(category.id)}/")
        print(response.json())
        assert response.status_code == 200
        assert response.json()["message"] == "Category deleted"
