# Django Rest Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

# users-login
from . import serializers


class HelloApiView(APIView):
    """ API View de prueba """
    serializer_class = serializers.HelloSerializer
    
    def get(self, request, format=None):
        """ Return a list of caracterictics """
        an_apiview = [
            'Usamos metodos HTTP como funciones (get, post, patch, put, delete)',
            'Es similar a una vista tradicional de django',
            'Nos da el mayor control sobre la logica de nuestra app',
            'Esta mapeado manualmente a los URLs'
        ]

        return Response(
            {
                'message': 'Hello World',
                'an_apiview': an_apiview
            }
        )
    
    def post(self, request):
        """ Create a message with our name """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def put(self, request, pk=None):
        """ Update an object, delete the old object and 
        create a new object with the information updated """
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """ Update an object """
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """ Delete an object """
        return Response({'method': 'DELETE'})


class HelloViewSet(ModelViewSet):
    """ View Set de prueba """
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """ Returns a message """
        a_viewset = [
            'Usa acciones (list, create, retrieve, update, partial_update)',
            'Automaticamente mapea a los URLs usando routers',
            'Provee mas funcionalidad con menos codigo'
        ]

        return Response({'message': 'Holaa', 'a_viewset': a_viewset})
    
    def create(self, request):
        """ Create a new message """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def retrieve(self, request, pk=None):
        """ Returns an object with your pk """
        return Response({'http_method': 'GET'})
    
    def update(self, request, pk=None):
        """ Update an object with your pk """
        return Response({'http_method': 'PUT'})
    
    def partial_update(self, request, pk=None):
        """ Update an object with your pk """
        return Response({'http_method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        """ Delete an object with your pk """
        return Response({'http_method': 'DELETE'})
