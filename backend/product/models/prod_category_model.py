from mongoengine import Document, StringField, DateTimeField
from django.utils import timezone 

class ProductCategory(Document):
    title = StringField(required=True, unique=True)
    description = StringField()
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super(ProductCategory, self).save(*args, **kwargs)
