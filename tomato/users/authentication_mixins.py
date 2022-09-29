# Django Rest Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

# users
from .authentication import ExpiringTokenAuthentication


class Authentication(object):
    user = None
    token_expired = False

    def get_user(self, request):
        """
        Returns the user with the associated token.If the user is not found,
        a response is returned
        """

        token = get_authorization_header(request).split()
        
        try:
            token = token[1].decode()
        
        except:
            response = Response(
                {
                    'error': 'Token was not sent'
                },
                status = status.HTTP_409_CONFLICT
                )
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = 'application/json'
            response.renderer_context = {}
            
            return response
        
        token_expire = ExpiringTokenAuthentication()
        try:
            user, token, self.token_expired = token_expire.authenticate_credentials(token)
        
        except AuthenticationFailed as e:
            response = Response(
                {
                    'error': e.get_full_details()['message']
                },
                status = status.HTTP_401_UNAUTHORIZED
                )
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = 'application/json'
            response.renderer_context = {}
            
            return response
        
        else:
            self.user = user

    def dispatch(self, request, *args, **kwargs):
        response = self.get_user(request)
        
        if isinstance(response, Response):
            # get_user() returned a response with a error message
            return response
        
        if self.user:
            return super().dispatch(request, *args, **kwargs)
    