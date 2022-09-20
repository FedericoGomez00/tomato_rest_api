# Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# products
from . import views


router = DefaultRouter()
router.register(r'', views.ProductViewSet, basename = 'products')


app_name = "products"
urlpatterns = [
    path('', include(router.urls)),
    # path('', views.ProductListCreateApiView.as_view(), name="list_create"),
    # path('all/', views.ProductListAllApiView.as_view(), name="list_all"),
    # path('<int:pk>/', views.ProductRetrieveUpdateDestroyApiView.as_view(), name="retrieve_update_destroy"),
]