# Django Rest Framework
from rest_framework import serializers

# products
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        exclude = ('is_available',)
    
    def validate_price(self, value):
        if value < 200:
            raise serializers.ValidationError("The price must be greater than or equal to 200")
        return value