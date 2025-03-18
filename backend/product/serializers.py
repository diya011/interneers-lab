from rest_framework import serializers
from .models import Product
from bson import ObjectId

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField(max_length=255)
    price = serializers.FloatField()
    brand = serializers.CharField(required=False, allow_blank=True)
    quantity = serializers.IntegerField()

    #to convert MongoEngine doc to JSON format
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id) if isinstance(instance.id, ObjectId) else instance.id
        return data

    #creating a new prod
    def create(self, validated_data):
        return Product(**validated_data).save()

    #Updating an existing prod
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance