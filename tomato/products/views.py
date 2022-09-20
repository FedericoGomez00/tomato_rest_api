# Django
from django.shortcuts import get_object_or_404

# Django Rest Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

# products
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    """ CRUD for product model. You can list, create, update and destroy """
    serializer_class = ProductSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_available = True)

    def list(self, request):
        """
        List products


        List the available products with stock greater than 0
        """
        serializer = self.get_serializer(
            self.get_queryset().filter(stock__gte = 1),
            many = True
            )

        return Response(
            serializer.data,
            status = status.HTTP_200_OK
            )
    
    def create(self, request):
        """
        Create a product


        Create a model row in the database
        """
        return super().create(request)
    
    def retrieve(self, request, pk=None):
        """
        List a product


        Retrieve a particular model row
        """
        row = get_object_or_404(
            self.get_serializer().Meta.model,
            id = pk
            )
        serializer = self.get_serializer(row)
        
        return Response(
            serializer.data,
            status = status.HTTP_200_OK
            )

    def update(self, request, pk=None):
        """
        Update a product


        Update a particular model row
        """
        return super().update(request, pk)
    
    # def partial_update(self, request, pk=None):
    #     """
    #     Partially upgrade a product


    #     Update a particular model row
    #     """
    #     return super().partial_update(request, pk)

    def destroy(self, request, pk=None):
        """
        Destroy a product


        Put False in is_available -> is_available = False
        """
        model = self.serializer_class.Meta.model
        product = get_object_or_404(model, id = pk)
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


# GENERIC IMPLEMENTATION

# ## List - Create
# class ProductListCreateApiView(ListCreateAPIView):
#     """ List the available products with stock greater than 0 """
#     serializer_class = ProductSerializer

#     def get_queryset(self):
#         model = self.get_serializer().Meta.model
#         return model.objects.filter(is_available = True).filter(stock__gte = 1)


# ## List all
# class ProductListAllApiView(ListAPIView):
#     """ List all available products in the database """
#     serializer_class = ProductSerializer
    
#     def get_queryset(self):
#         model = self.get_serializer().Meta.model
#         return model.objects.filter(is_available = True)


# ## Retrieve - Update - Destroy
# class ProductRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
#     """ Retrieve, update or destroy a particular model row """
#     serializer_class = ProductSerializer
#     queryset = serializer_class.Meta.model.objects.filter(is_available = True)

#     def delete(self, request, pk=None):
#         """ Put False in is_available """
#         try:
#             product = self.queryset.get(id = pk)
#         except ObjectDoesNotExist:
#             return Response(
#             {'error': 'The product was not found'},
#             status = status.HTTP_400_BAD_REQUEST
#             )
#         else:
#             product_serializer = self.serializer_class(product)
#             product.is_available = False
#             product.save()
#             return Response(
#                 {
#                     'message': 'The product destroyed',
#                     'product': product_serializer.data
#                 },
#                 status = status.HTTP_200_OK
#                 )
