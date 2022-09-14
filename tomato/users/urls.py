# Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# users
from . import views


router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('profile', views.UserProfileViewSet)
    ## no se coloca basename xq en el viewset definimos un queryset


app_name = "users"
urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view(), name="hello"),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('register/', views.UserRegisterApiView.as_view(), name='register'),
    path('', include(router.urls))
]
