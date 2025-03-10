from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator

PRODUCTS = []                                            #products lists for in-memory operation

def validate_product_data(data):
    errors = {}                                          #to store errors

    if not data.get("name"):
        errors["name"] = "Product name is required."
    if not data.get("category"):
        errors["category"] = "Category is required."
    if not data.get("brand"):
        errors["brand"] = "Brand is required."
    if not data.get("price"):
        errors["price"] = "Price is required."
    
    try:
        price = float(data.get("price", 0))
        if price <= 0:
            errors["price"] = "Price should be +ve."
    except ValueError:
        errors["price"] = "Invalid price format"

    try:
        quantity = int(data.get("quantity", 0))
        if quantity < 0:
            errors["quantity"] = "Quantity can't be -ve."
    except ValueError:
        errors["quantity"] = "Invalid quantity format."

    return errors

# Creating a new prod
@csrf_exempt                                                       #to disable csrf protection so that Postman can make successful request
def create_product(request):
    if request.method == "POST":                                   #for validation of API's
        try:
            data = json.loads(request.body)
            errors = validate_product_data(data)    
            if errors:
                return JsonResponse({"errors": errors}, status=400)
            product_id = len(PRODUCTS) + 1
            product = {
                "id": product_id,
                "name": data["name"],
                "brand": data["brand"],
                "description": data.get("description", ""),
                "category": data["category"],
                "price": float(data["price"]),
                "quantity": int(data["quantity"]),
                "mfg_date":data["mfg_date"],
                "expiry_date":data["expiry_date"]
            }
            PRODUCTS.append(product)
            return JsonResponse({"message": "Product created successfully!", "product": product}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    return JsonResponse({"error": "Can't perform this funcn"}, status=405)

@csrf_exempt
# Fetching a list of products
def get_product_list(request):
    if request.method == "GET":
        page = int(request.GET.get("page", 1))  
        limit = int(request.GET.get("limit", 2))

        paginator = Paginator(PRODUCTS, limit)                       #to paginate with a limit
        try:
            products_page = list(paginator.page(page))
        except Exception:
            return JsonResponse({"error": "Invalid page number"}, status=400)
        
        return JsonResponse({
            "total_pages": paginator.num_pages,                      #to show the total no. of pages : by default it will show 1
            "products": products_page}, status=200,)                 #to show the limit no. of products
        
    return JsonResponse({"errors": "Can't perform this funcn"} , status=405)

@csrf_exempt
# Fetching a single product by index
def get_product(request, index):
    if request.method=="GET" :
        if index < 0 or index >= len(PRODUCTS):
            return JsonResponse({"error": "Product not found"}, status=404)
        return JsonResponse(PRODUCTS[index], status=200)
    return JsonResponse({"error": "Can't perform this funcn"}, status=405)

# Updating a product
@csrf_exempt
def update_product(request, index):
    if request.method == "PUT":
        try:
            if index < 0 or index >= len(PRODUCTS):
                return JsonResponse({"error": "Product not found"}, status=404)

            data = json.loads(request.body)
            errors = validate_product_data(data)
            if errors:
                return JsonResponse({"errors": errors}, status=400)

            PRODUCTS[index].update(data)
            return JsonResponse({"message": "Product updated successfully!",
                                 "product": PRODUCTS[index]}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Can't perform this funcn"}, status=405)

# Deleting a product
@csrf_exempt
def delete_product(request, index):
    if request.method == "DELETE" :
        if index < 0 or index >= len(PRODUCTS):
            return JsonResponse({"error": "Product not found"}, status=404)

        deleted_product = PRODUCTS.pop(index)
        return JsonResponse({"message": "Product deleted successfully!", 
                             "deleted_product": deleted_product}, status=200)

    return JsonResponse({"error": "Can't perform this funcn"}, status=405)
