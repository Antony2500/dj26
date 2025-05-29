from django.urls import path

from .views import index, test_login, first_custom_form, second_custom_form, register_user, logout_user

urlpatterns = [
    path("", index, name="index"),
    path("test_login", test_login),
    path("form", first_custom_form, name="form"),
    path("form2", second_custom_form, name="form2"),
    path("register", register_user),
    path("logout", logout_user, name="custom_logout")
]