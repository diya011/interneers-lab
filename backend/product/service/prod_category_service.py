from product.repository.prod_category_repository import ProductCategoryRepository

class ProductCategoryService:

    @staticmethod
    def create_category(data):
        return ProductCategoryRepository.create(data)

    @staticmethod
    def get_all_categories():
        return ProductCategoryRepository.get_all()

    @staticmethod
    def get_category_by_id(category_id):
        return ProductCategoryRepository.get_by_id(category_id)

    @staticmethod
    def update_category(category_id, data):
        return ProductCategoryRepository.update(category_id, data)

    @staticmethod
    def delete_category(category_id):
        return ProductCategoryRepository.delete(category_id)