# Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# users
from .views import *


router = DefaultRouter()
router.register('profile', UserProfileViewSet) ## no se coloca basename xq en el viewset definimos un queryset


app_name = "users"
urlpatterns = [
    # path('register/', UserRegisterApiView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('logout/', UserLogoutApiView.as_view(), name='logout'),
    path('', include(router.urls)),
]
