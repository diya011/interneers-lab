from .models import Product

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
