from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .service import ProductService
from .serializers import ProductSerializer
from bson import ObjectId

#Creates a new product and returns its id
@csrf_exempt
def create_product(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product = ProductService.create_product(data)
            return JsonResponse({"message": "Product created", "id": str(product.id)}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

#to get a product by id
def get_product(request, product_id):
    try:
        product = ProductService.get_product(ObjectId(product_id))
        if product:
            return JsonResponse(ProductSerializer(product).data, safe=False)
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

#to list all products
def get_product_list(request):
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
