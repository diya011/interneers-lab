from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.cache import never_cache

@never_cache
def hello_name(request):
    """
    A simple view that returns 'Hello, {name}' in JSON format.
    Uses a query parameter named 'name'.
    """
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "unsung")
    city = request.GET.get("city", "secret")
    return JsonResponse({"message": f"Hey! I'm {name} from {city} :)"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name), 
    # Example usage: /hello/?name=Bob
    # returns {"message": "Hello, Bob!"}
]
