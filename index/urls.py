from Tools.scripts.make_ctype import method
from django.urls import path

from .views import (index, test_login, first_custom_form,
                    second_custom_form, register_user, logout_user,
                    get_stuff, get_all_stuff, create_stuff, get_or_create_stuff, update_stuff, delete_stuff,
                    request_info_check, redirect_view, info_view, AboutUs, StuffListView, get_all_stuff2,
                    create_new_product, book_edit_view, create_book_view_set, my_view, test_signal, create_article,
                    send_mail_console, bad_request, reset_password
                    )

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
    path("delete/<int:id_>", delete_stuff),
    path("get", request_info_check),

    path("redirect_view/<int:pk>/<str:stuff_name>", redirect_view),
    path("info_view/<int:pk>/<str:stuff_name>", info_view, name="info_stuff"),
    path("about_us", AboutUs.as_view()),
    path("stuff", StuffListView.as_view()),

    path("all_stuff", get_all_stuff2),
    path("2", create_new_product),
    path("formset", book_edit_view, name="book_formset"),
    path("create_book_view_set", create_book_view_set, name="create_book_formset"),
    path("my_view", my_view),
    path("test_signal", test_signal),
    path("test-signal2", create_article),
    path("email", send_mail_console),
    path("400", bad_request, name="400_bad_request"),
    path("reset_password", reset_password)
]
