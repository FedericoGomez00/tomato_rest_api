# Django
from django.contrib import admin

# products
from .models import UserProfile


admin.site.register(UserProfile)