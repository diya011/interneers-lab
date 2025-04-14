from bson import ObjectId
from product.repository.prod_category_repository import ProductCategoryRepository
from product.models.prod_model import Product

class ProductRepository:
    @staticmethod
    def create_product(data):
        product = Product(**data)
        product.save()
        return product         

    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects(id=product_id).first()

    @staticmethod
    def get_all_products():
        return list(Product.objects.all())

    @staticmethod
    def update_product(product_id, data):
        product = Product.objects(id=product_id).first()
        if product:
            product.update(**data)
            return Product.objects(id=product_id).first()  # to fetch updated prod
        return None

    @staticmethod
    def delete_product(product_id):
        product = Product.objects(id=product_id).first()
        if product:
            product.delete()
            return True                                             
        return False
    
    @staticmethod
    def get_by_category(category_id):
        return Product.objects(category_id=category_id)
    
    @staticmethod
    def set_category(product_id, category_obj):
        product = Product.objects(id=ObjectId(product_id)).first()
        if product:
            product.category_id = category_obj
            product.save()
            return product
        return None

    @staticmethod
    def remove_category(product_id):
        product = Product.objects(id=ObjectId(product_id)).first()
        if product:
            product.category_id = None
            product.save()
            return product
        return None
