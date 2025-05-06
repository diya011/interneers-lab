from mongoengine import Document, StringField, FloatField, IntField , ReferenceField
# from product.models.prod_category_model import ProductCategory
from product.models.prod_category_model import ProductCategory
class Product(Document):
    name = StringField(required=True, max_length=255)
    description = StringField()
    # category = StringField(required=True)
    price = FloatField(required=True)
    brand = StringField(required=True , default="Unknown")
    quantity = IntField()
    category_id = ReferenceField(ProductCategory , null=True)

    def __str__(self):
        return self.name