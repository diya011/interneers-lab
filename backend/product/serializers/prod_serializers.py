from rest_framework import serializers
from product.models.prod_model import Product
from bson import ObjectId
from product.models.prod_category_model import ProductCategory

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    category_id = serializers.CharField() 
    price = serializers.FloatField()
    brand = serializers.CharField(required=False, allow_blank=True)
    quantity = serializers.IntegerField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id) if isinstance(instance.id, ObjectId) else instance.id
        data['category_id'] = str(instance.category_id.id) if instance.category_id else None  
        return data

    def create(self, validated_data):
        category_id = validated_data.pop('category_id') 
        try:
            category_obj = ProductCategory.objects.get(id=ObjectId(category_id))
        except ProductCategory.DoesNotExist:
            raise serializers.ValidationError("Invalid category ID provided.")
        
        product = Product(category_id=category_obj, **validated_data) 
        product.save()
        return product

    def update(self, instance, validated_data):
        if 'category_id' in validated_data:
            category_id = validated_data.pop('category_id')
            try:
                instance.category_id = ProductCategory.objects.get(id=category_id)
            except ProductCategory.DoesNotExist:
                raise serializers.ValidationError("Invalid category ID for update.")

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
