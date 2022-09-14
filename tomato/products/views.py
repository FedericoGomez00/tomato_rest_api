# Django
from django.shortcuts import render

# Django Rest Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView

# products
from .models import Product
from .serializers import ProductSerializer


class ProductListApiView(ListAPIView):
    """ List the products with stock greater than 0 """
    serializer_class = ProductSerializer

    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.filter(stock__gte = 1)
    

class ProductCreateApiView(CreateAPIView):
    """ Create a product """
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(stock__gte = 1)

    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'The product was created successfully'},
                status = status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
            )