# Django
from django.contrib import admin

# blog
from .models import BlogPost


admin.site.register(BlogPost)