# Django
from django.urls import path

# Django Rest Framework
# from rest_framework.routers import DefaultRouter

# products
from . import views


app_name = "products"
urlpatterns = [
    path('', views.ProductListApiView.as_view(), name="list"),
    path('create/', views.ProductCreateApiView.as_view(), name="create"),
]
