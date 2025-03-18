from django.urls import path
from .views import create_product, get_product, get_product_list, update_product, delete_product

urlpatterns = [
    path('create/', create_product, name='create_product'),
    path('list/', get_product_list, name='get_product_list'),
    path('<str:product_id>/', get_product, name='get_product'),
    path('update/<str:product_id>/', update_product, name='update_product'),          #bcoz we are using auto generated hex id by ObjectId
    path('delete/<str:product_id>/', delete_product, name='delete_product'),
]
