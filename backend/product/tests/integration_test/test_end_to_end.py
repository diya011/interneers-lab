from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from bson import ObjectId
import json
from product.models.prod_model import Product
from product.models.prod_category_model import ProductCategory

class ProductCategoryAPITests(TestCase):
    def setUp(self):
        # Create a sample category for testing
        self.category_data = {"title": "Electronics"}
        self.category_url = reverse("create_category")
        
        self.product_data = {
            "name": "Smartphone",
            "price": 500,
            "brand": "BrandX",
            "quantity": 10,
            "category_id": None,  
        }
        self.product_url = reverse("create_product")
        
        self.client.post(self.category_url, self.category_data, content_type="application/json")

    def test_create_category(self):
        """Test creating a new category"""
        response = self.client.post(self.category_url, self.category_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Category created", response.json().get("message"))

    def test_get_all_categories(self):
        """Test getting all categories"""
        # First, create a category
        self.client.post(self.category_url, self.category_data, content_type="application/json")
        response = self.client.get(reverse("get_all_categories"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.json()), 0)  # Check if there's at least one category

    def test_get_category_by_id(self):
        """Test getting a category by ID"""
        category_response = self.client.post(self.category_url, self.category_data, content_type="application/json")
        category_id = category_response.json().get("id")
        response = self.client.get(reverse("get_category_by_id", args=[category_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], "Electronics")

    def test_update_category(self):
        """Test updating an existing category"""
        category_response = self.client.post(self.category_url, self.category_data, content_type="application/json")
        category_id = category_response.json().get("id")
        updated_data = {"title": "Updated Electronics"}
        response = self.client.put(reverse("update_category", args=[category_id]), 
                                   updated_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Category updated", response.json().get("message"))

    def test_delete_category(self):
        """Test deleting a category"""
        category_response = self.client.post(self.category_url, self.category_data, content_type="application/json")
        category_id = category_response.json().get("id")
        response = self.client.delete(reverse("delete_category", args=[category_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Category deleted", response.json().get("message"))

    def test_create_product(self):
        """Test creating a new product"""
        category_response = self.client.post(self.category_url, self.category_data, content_type="application/json")
        category_id = category_response.json().get("id")
        self.product_data["category_id"] = category_id  # Assigning category ID correctly
        response = self.client.post(self.product_url, self.product_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Product created", response.json().get("message"))

    def test_get_product(self):
        """Test getting a product by ID"""
        category = ProductCategory.objects.first()
        product = Product.objects.create(
            name="Laptop", price=800, brand="BrandY", quantity=5, category_id=category  
        )
        response = self.client.get(reverse("get_product", args=[str(product.id)]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], product.name)

    def test_get_product_list(self):
        """Test getting the list of products"""
        category_response = self.client.post(self.category_url, self.category_data, content_type="application/json")
        category_id = category_response.json().get("id")  # Get the ID of the created category
        self.product_data["category_id"] = category_id
        response = self.client.post(self.product_url, self.product_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse("get_product_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.json()), 0)

    def test_update_product(self):
        """Test updating a product"""
        # Create a category
        category_response = self.client.post(self.category_url, self.category_data, content_type="application/json")
        category_id = category_response.json().get("id")
        
        # Create a product and associate it with the category
        product_response = self.client.post(self.product_url, {
            **self.product_data, "category_id": category_id}, content_type="application/json")
        product_id = product_response.json().get("id")
        
        # Prepare updated product data
        updated_data = {
            "name": "Updated Laptop",
            "price": 900,
            "brand": "BrandZ",
            "quantity": 10,
            "category_id": category_id  # Ensure category_id is passed for update
        }
    
        # Make the update request
        response = self.client.put(reverse("update_product", args=[str(product_id)]), updated_data, content_type="application/json")
        
        # Check if the update is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Product updated", response.json().get("message"))


    def test_delete_product(self):
        """Test deleting a product"""
        category = ProductCategory.objects.first()
        product = Product.objects.create(
            name="Laptop", price=800, brand="BrandY", quantity=5, category_id=category  # Fix the field name to category_id
        )
        response = self.client.delete(reverse("delete_product", args=[str(product.id)]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Product deleted", response.json().get("message"))

    def test_add_product_to_category(self):
        """Test adding a product to a category"""
        category = ProductCategory.objects.first()
        if category is None:
            raise ValueError("No ProductCategory found in the database.")
        product = Product.objects.create(
            name="Smart Watch", price=150, brand="BrandZ", quantity=5
        )
        response = self.client.put(
            reverse("add_product_to_category", args=[str(product.id), str(category.id)]),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Product added to category successfully", response.json().get("message"))

    def test_remove_product_from_category(self):
        """Test removing a product from a category"""
        category = ProductCategory.objects.first()
        product = Product.objects.create(
            name="Smart Watch", price=150, brand="BrandZ", quantity=5, category_id=category  # Fix the field name to category_id
        )
        response = self.client.put(
            reverse("remove_product_from_category", args=[str(product.id)]),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Product removed from category successfully", response.json().get("message"))
    
    def test_get_products_by_category(self):
        """Test getting products by category"""
        # Create a category
        category_response = self.client.post(self.category_url, self.category_data, content_type="application/json")
        category_id = category_response.json().get("id")

        # Create a product and associate it with the category
        product_response = self.client.post(self.product_url, {
            **self.product_data, "category_id": category_id}, content_type="application/json")
        self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)

        # Get the list of products for this category
        response = self.client.get(reverse("get_products_by_category", args=[str(category_id)]))

        # Ensure products are returned for the category
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.json()), 0)  # Check if there are products in the category

