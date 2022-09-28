# Python
from datetime import datetime

# Django
from django.contrib.sessions.models import Session

# Django Rest Framework
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
# from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.authentication import get_authorization_header

# users
from .serializers import *
# from .permissions import *


class UserProfileViewSet(ModelViewSet):
    """
    Create and update profiles
    """
    serializer_class = UserProfileSerializer
    queryset = serializer_class.Meta.model.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permissions_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email', 'username')


# API View de prueba para registrar usuarios
class UserRegisterApiView(APIView):
    serializer_class = UserProfileSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            user = serializer.data
            print(user)
            serializer.data.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)


class UserLoginApiView(ObtainAuthToken):
    """
    Log In

    The users can login to the app with username and password
    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        """
        Log In
        
        Log in with username and password.

        The token is renewed at login.
        If the user has an active session, they can't log in
        """

        # Use AuthTokenSerializer -> validate username and password
        login_serializer = self.serializer_class(
            data = request.data,
            context = {'request': request}
            )
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            user_serializer = UserProfileSerializer(user)
            
            if user.is_active:
                token,created = Token.objects.get_or_create(user = user)

                message = 'Successful login.'

                if not created:
                    # Renueva el token
                    token.delete()
                    token = Token.objects.create(user = user)

                    message = message + ' The token was renewed.'
                
                return Response(
                    {
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': message
                    },
                    status = status.HTTP_201_CREATED
                    )
            
            return Response(
                {
                    'error': 'This user is not active',
                    'user': user_serializer.data['username']
                },
                status = status.HTTP_401_UNAUTHORIZED
                )
        
        return Response(
            {'error': 'The credentials are not correct'},
            status = status.HTTP_400_BAD_REQUEST
            )


class UserLogoutApiView(APIView):
    """
    Log Out

    The users can log out sending your token
    """
    serializer_class = UserProfileSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_active = True)
    
    def get(self, request, *args, **kwargs):
        """
        Log Out

        Send the token in the token variable

        Params
            - token = token
        """
        
        token = request.GET.get('token')
        
        if token == '' or token == None:
            return Response(
            {
                'error': 'The token was not sent'
            },
            status = status.HTTP_409_CONFLICT
            )

        try:
            token = Token.objects.get(key = token)
            user = token.user
        
        except:
            return Response(
                {
                    'error': 'A user with those credential was not found'
                },
                status = status.HTTP_400_BAD_REQUEST
                )
        
        else:
            # Eliminar sesiones
            all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
            if all_sessions.exists():
                for session in all_sessions:
                    session_data = session.get_decoded()
                    if user.id == int(session_data.get('_auth_user_id')):
                        session.delete()
                
            token.delete()

            return Response(
                {
                    'token_message': 'Token deleted',
                    'session_message': 'User sessions deleted'
                },
                status = status.HTTP_200_OK
                )
