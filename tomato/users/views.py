# Python
from datetime import datetime

# Django
from django.contrib.sessions.models import Session

# Django Rest Framework
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings

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
        login_serializer = self.serializer_class(
            data = request.data,
            context = {'request': request}
            )
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            
            if user.is_active:
                token,created = Token.objects.get_or_create(user = user)
                user_serializer = UserProfileSerializer(user)

                if not created:
                    # # Renueva el token
                    # token.delete()
                    # token = Token.objects.create(user = user)

                    # No permite tener dos sesiones activas
                    return Response(
                    {
                        'error': 'The user already has an active session'
                    },
                    status = status.HTTP_409_CONFLICT
                    )
                
                return Response(
                    {
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Successful login'
                    },
                    status = status.HTTP_201_CREATED
                    )
            
            return Response(
                {'error': 'This user is not active'},
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
    queryset = serializer_class.Meta.model.objects.all()
    
    def get(self, request, *args, **kwargs):
        """
        Log Out

        Send the token in the token variable

        Params
            - token = token
        """
        
        token = request.GET.get('token')

        if token == '':
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
                    'token_message': 'The token deleted',
                    'session_message': 'The sessions deleted'
                },
                status = status.HTTP_200_OK
                )


# API View de prueba para registrar usuarios
class UserRegisterApiView(APIView):
    serializer_class = UserProfileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)