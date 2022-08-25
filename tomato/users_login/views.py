from rest_framework.views import APIView
from rest_framework.response import Response


class HelloApiView(APIView):
    """ API View de prueba """

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