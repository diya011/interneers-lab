from django.urls import path
from .views import (
    create_product, get_product, get_product_list,
    update_product, delete_product,
    create_category, get_all_categories, get_category_by_id,
    delete_category, update_category, get_products_by_category,
    add_product_to_category , remove_product_from_category
)

urlpatterns = [
    # Below are Product model APIs
    path('create/', create_product, name='create_product'),
    path('list/', get_product_list, name='get_product_list'),
    path('<str:product_id>/', get_product, name='get_product'), 
    path('update/<str:product_id>/', update_product, name='update_product'), 
    path('delete/<str:product_id>/', delete_product, name='delete_product'), 
    path('get_category/<str:category_id>/', get_products_by_category, name='get_products_by_category'), 
    path('<str:product_id>/add_to_category/<str:category_id>/', add_product_to_category, name='add_product_to_category'),
    path('<str:product_id>/remove_from_category/', remove_product_from_category, name='remove_product_from_category'),

    # Below are Category model APIs
    path('category/create/', create_category, name='create_category'),
    path('category/all/', get_all_categories, name='get_all_categories'),
    path('category/get/<str:category_id>/', get_category_by_id, name='get_category_by_id'),
    path('category/update/<str:category_id>/', update_category, name='update_category'),
    path('category/delete/<str:category_id>/', delete_category, name='delete_category'),
]
