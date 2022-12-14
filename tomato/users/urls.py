# Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# users
from .views import *


router = DefaultRouter()
router.register('profile', UserProfileViewSet)


app_name = "users"
urlpatterns = [
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('logout/', UserLogoutApiView.as_view(), name='logout'),
    path('refresh-token/', UserToken.as_view(), name='refresh_token'),
    path('recover-password/', recover_password, name = 'recover_password'),
    path('', include(router.urls)),
]
