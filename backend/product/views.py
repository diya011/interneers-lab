from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from product.serializers.prod_serializers import ProductSerializer
from bson import ObjectId

from product.service.prod_category_service import ProductCategoryService
from product.serializers.prod_category_serializers import ProductCategorySerializer
from product.service.prod_service import ProductService

from product.models.prod_model import Product
from product.models.prod_category_model import ProductCategory

def validate_product_data(data):
    required_fields = ["name", "price", "brand", "quantity"]
    for field in required_fields:
        if field not in data:
            return f"{field} is required"

    if not isinstance(data["price"], (int, float)) or data["price"] < 0:
        return "Price must be a non-negative number"

    if not isinstance(data["quantity"], int) or data["quantity"] < 0:
        return "Quantity must be a non-negative integer"

    return None


def validate_category_data(data):
    if "title" not in data or not data["title"].strip():
        return "Title is required"
    return None


@csrf_exempt
#creating a new category
def create_category(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            validation_error = validate_category_data(data)
            if validation_error:
                return JsonResponse({"error": validation_error}, status=400)
            category = ProductCategoryService.create_category(data)
            return JsonResponse({"message": "Category created", "id": str(category.id)}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
#getting all categories present
def get_all_categories(request):
    if request.method == "GET":
        try:
            categories = ProductCategoryService.get_all_categories()
            serialized = [ProductCategorySerializer(cat).data for cat in categories]
            return JsonResponse(serialized, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
#getting only specified category
def get_category_by_id(request, category_id):
    if request.method == "GET":
        try:
            category = ProductCategoryService.get_category_by_id(category_id)
            if category:
                return JsonResponse(ProductCategorySerializer(category).data)
            return JsonResponse({"error": "Not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
#updating the fields in a category
def update_category(request, category_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            validation_error = validate_category_data(data)
            if validation_error:
                return JsonResponse({"error": validation_error}, status=400)

            updated_category = ProductCategoryService.update_category(category_id, data)
            if updated_category:
                return JsonResponse({"message": "Category updated"})
            return JsonResponse({"error": "Category not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
#deleting the category
def delete_category(request, category_id):
    if request.method == "DELETE":
        try:
            success = ProductCategoryService.delete_category(category_id)
            if success:
                return JsonResponse({"message": "Category deleted"})
            return JsonResponse({"error": "Category not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)



#Creates a new product and returns its id
@csrf_exempt
def create_product(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            validation_error = validate_product_data(data)
            if validation_error:
                return JsonResponse({"error": validation_error}, status=400)

            # Call the service to create the product
            product = ProductService.create_product(data)
            return JsonResponse({"message": "Product created", "id": str(product.id)}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


#to get a product by id
@csrf_exempt
def get_product(request, product_id):
    try:
        product = ProductService.get_product(ObjectId(product_id))
        if product:
            return JsonResponse(ProductSerializer(product).data, safe=False)
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

#to list all products
@csrf_exempt
def get_product_list(request):
    if request.method == "GET":
        try:
            products = ProductService.get_all_products()
            serialized_products = [ProductSerializer(product).data for product in products]
            return JsonResponse(serialized_products, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
#to update a product
def update_product(request, product_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            validation_error = validate_product_data(data)
            if validation_error:
                return JsonResponse({"error": validation_error}, status=400)
            
            updated_product = ProductService.update_product(ObjectId(product_id), data)
            if updated_product:
                return JsonResponse({"message": "Product updated"})
            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


#to delete a product
@csrf_exempt
def delete_product(request, product_id):
    if request.method == "DELETE":
        try:
            success = ProductService.delete_product(ObjectId(product_id))
            if success:
                return JsonResponse({"message": "Product deleted"})
            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt    
def get_products_by_category(request, category_id):
    if request.method == "GET":
        try:
            products = ProductService.get_products_by_category(ObjectId(category_id))
            serialized = [ProductSerializer(prod).data for prod in products]
            return JsonResponse(serialized, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
@csrf_exempt
def add_product_to_category(request, product_id, category_id):
    if request.method == "PUT":
        try:
            category = ProductCategory.objects(id=category_id).first()
            if not category:
                return JsonResponse({"error": "Category not found"}, status=404)

            result = ProductService.add_product_to_category(product_id, category)

            if result:
                return JsonResponse({"message": "Product added to category successfully"})
            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def remove_product_from_category(request, product_id):
    if request.method == "PUT":
        try:
            result = ProductService.remove_product_from_category(product_id)
            if result:
                return JsonResponse({"message": "Product removed from category successfully"})
            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)