# Django
from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# blog
from .views import *


router = DefaultRouter()
router.register(r'', BlogpostViewSet, basename = 'blogposts')


app_name = "blog"
urlpatterns = [
    path('', include(router.urls)),
    # path('like/<int:pk>', LikeBlogpost.as_view(), name="like_blogpost"),
]