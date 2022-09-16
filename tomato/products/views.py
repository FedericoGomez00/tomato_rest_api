# Django
from django.core.exceptions import ObjectDoesNotExist

# Django Rest Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

# products
from .serializers import ProductSerializer


## List - Create
class ProductListCreateApiView(ListCreateAPIView):
    """ List the available products with stock greater than 0 """
    serializer_class = ProductSerializer

    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.filter(is_available = True).filter(stock__gte = 1)


## List all
class ProductListAllApiView(ListAPIView):
    """ List all available products in the database """
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.filter(is_available = True)


## Retrieve - Update - Destroy
class ProductRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    """ Retrieve, update or destroy a particular model row """
    serializer_class = ProductSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_available = True)

    def delete(self, request, pk=None):
        """ Put False in is_available """
        try:
            product = self.queryset.get(id = pk)
        except ObjectDoesNotExist:
            return Response(
            {'error': 'The product was not found'},
            status = status.HTTP_400_BAD_REQUEST
            )
        else:
            product_serializer = self.serializer_class(product)
            product.is_available = False
            product.save()
            return Response(
                {
                    'message': 'The product destroyed',
                    'product': product_serializer.data
                },
                status = status.HTTP_200_OK
                )
