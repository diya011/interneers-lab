from mongoengine import Document, StringField, FloatField, IntField

# Define Product Model
class Product(Document):
    name = StringField(required=True, max_length=255)
    description = StringField()
    category = StringField(required=True)
    price = FloatField(required=True)
    brand = StringField(required=True)
    quantity = IntField(required=True)

    def __str__(self):
        return self.name