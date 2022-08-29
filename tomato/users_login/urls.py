# Django
from django.urls import path, include
from users_login import views

# Django Rest Framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')


app_name = "users_login"
urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view(), name="hello"),
    path('', include(router.urls))
]
