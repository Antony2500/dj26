from django.urls import path

from .views import index, test_login

urlpatterns = [
    path("", index, name="index"),
    path("test_login", test_login)
]