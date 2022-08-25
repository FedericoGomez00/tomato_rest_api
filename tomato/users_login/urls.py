from django.urls import path
from users_login import views

app_name = "users_login"
urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
]
