from django.urls import path
from .views import create_product, get_product_list, get_product, update_product, delete_product

urlpatterns = [
    path("create/", create_product, name="create_product"),                #to create prod
    path("list/", get_product_list, name="get_product_list"),              #to fetch list of prod
    path("get/<int:index>/", get_product, name="get_product"),             #to fetch a single prod
    path("update/<int:index>/", update_product, name="update_product"),    #to update a prod of specified index
    path("delete/<int:index>/", delete_product, name="delete_product"),    #to delete a prod of specified index
]