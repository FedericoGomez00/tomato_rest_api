# Django Rest Framework
from rest_framework import serializers

# blog
from .models import BlogPost


class BlogpostSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost
        exclude = ('created', 'is_active')


# class BlogpostListSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = BlogPost
#         fields = '__all__'