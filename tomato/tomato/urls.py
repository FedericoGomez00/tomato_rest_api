# Django
from django.contrib import admin
from django.urls import path, re_path, include

# Django Rest Framework
from rest_framework import permissions

# drf-yasg
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


# Docs
schema_view = get_schema_view(
    openapi.Info(
        title = "Tomato API",
        default_version='v0.1',
        description="Tomato is an e-comerce and blog",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@tomato.com"),
        license=openapi.License(name="BSD License"),
        ),
    public = True,
    permission_classes = [permissions.AllowAny],
)


drf_yasg_urls = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

tomato_urls = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include("users.urls")),
    path('products/', include("products.urls")),
    path('blog/', include("blog.urls")),
    ]

urlpatterns = drf_yasg_urls + tomato_urls