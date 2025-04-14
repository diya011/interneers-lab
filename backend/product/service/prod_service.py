from product.repository.prod_repository import ProductRepository

class ProductService:
    @staticmethod
    def create_product(data):
        return ProductRepository.create_product(data)

    @staticmethod
    def get_product(product_id):
        return ProductRepository.get_product_by_id(product_id)

    @staticmethod
    def get_all_products():
        return ProductRepository.get_all_products()

    @staticmethod
    def update_product(product_id, data):
        return ProductRepository.update_product(product_id, data)

    @staticmethod
    def delete_product(product_id):
        return ProductRepository.delete_product(product_id)
    
    @staticmethod
    def get_products_by_category(category_id):
        return ProductRepository.get_by_category(category_id)
    
    @staticmethod
    def add_product_to_category(product_id , category_id):
        return ProductRepository.set_category(product_id , category_id)
    
    @staticmethod
    def remove_product_from_category(product_id , category_id):
        return ProductRepository.remove_category(product_id , category_id)
