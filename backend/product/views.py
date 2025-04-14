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

@csrf_exempt
#creating a new category
def create_category(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
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
            if not data.get("brand"):
                return JsonResponse({"error": "Brand is required"}, status=400)
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
            product = Product.objects(id=product_id).first()
            category = ProductCategory.objects(id=category_id).first()

            if not product:
                return JsonResponse({"error": "Product not found"}, status=404)
            if not category:
                return JsonResponse({"error": "Category not found"}, status=404)

            product.category_id = category
            product.save()
            return JsonResponse({"message": "Product added to category successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def remove_product_from_category(request, product_id):
    if request.method == "PUT":
        try:
            product = Product.objects(id=product_id).first()

            if not product:
                return JsonResponse({"error": "Product not found"}, status=404)

            product.category_id = None
            product.save()
            return JsonResponse({"message": "Product removed from category successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

