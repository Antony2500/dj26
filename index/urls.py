from django.urls import path

from .views import (index, test_login, first_custom_form,
                    second_custom_form, register_user, logout_user,
                    get_stuff, get_all_stuff, create_stuff, get_or_create_stuff, update_stuff, delete_stuff)

urlpatterns = [
    path("", index, name="index"),
    path("test_login", test_login),
    path("form", first_custom_form, name="form"),
    path("form2", second_custom_form, name="form2"),
    path("register", register_user),
    path("logout", logout_user, name="custom_logout"),
    path("car/<int:id_>", get_stuff),
    path("car/", get_all_stuff),
    path("create", create_stuff),
    path("get_or_create_stuff/<int:id_>", get_or_create_stuff),
    path("update/<int:id_>", update_stuff),
    path("delete/<int:id_>", delete_stuff)
]