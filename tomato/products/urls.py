# Django
from django.urls import path

# Django Rest Framework
# from rest_framework.routers import DefaultRouter

# products
from . import views


app_name = "products"
urlpatterns = [
    path('', views.ProductListCreateApiView.as_view(), name="list_create"),
    path('all/', views.ProductListAllApiView.as_view(), name="list_all"),
    path('<int:pk>/', views.ProductRetrieveUpdateDestroyApiView.as_view(), name="retrieve_update_destroy"),
]