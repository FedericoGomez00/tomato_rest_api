# Python
from datetime import timedelta

# Django
from django.utils import timezone

# Django Rest Framework
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

# tomato
from tomato.settings import TOKEN_EXPIRED_AFTER_SECONDS


class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Add an expiration time to the token
    """

    def expires_in(self, token):
        """ Calculate the expiration time """
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds = TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    def is_token_expired(self, token):
        """ Returns if the token was expired """
        return self.expires_in(token) < timedelta(seconds = 0)

    def token_expire_handler(self, token):
        is_expire = self.is_token_expired(token)
        if is_expire:
            print('Token expired')
        
        return is_expire

    def authenticate_credentials(self, key):
        try:
            token = self.get_model().objects.get(key = key)
        
        except self.get_model().DoesNotExist:
            raise AuthenticationFailed('Invalid token')
        
        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        is_expired = self.token_expire_handler(token)
        if is_expired:
            raise AuthenticationFailed('Token expired')
        
        return (token.user, token)