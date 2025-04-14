from product.models.prod_category_model import ProductCategory
from bson import ObjectId

class ProductCategoryRepository:

    @staticmethod
    def create(data):
        return ProductCategory(**data).save()

    @staticmethod
    def get_all():
        return ProductCategory.objects()

    @staticmethod
    def get_by_id(category_id):
        return ProductCategory.objects(id=ObjectId(category_id)).first()

    @staticmethod
    def update(category_id, update_data):
        return ProductCategory.objects(id=ObjectId(category_id)).update_one(**update_data)

    @staticmethod
    def delete(category_id):
        return ProductCategory.objects(id=ObjectId(category_id)).delete()