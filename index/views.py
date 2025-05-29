import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RenewBookForm, StuffForm, RegisterUser


def index(request):
    return render(request, "index.html", context={"title": "Main"})

def test_login(request):
    return render(request, "test_login.html", context={"title": "Main"})

def first_custom_form(request):
    if request.method == "POST":
        form = RenewBookForm(request.POST)

        if form.is_valid():
            return redirect("index")

        messages.error(request, "Invalid form data. Plz rewrite ")
        return redirect("form")

    proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
    form = RenewBookForm(initial={"renewal_date": proposed_renewal_date})

    context = {"form": form}

    return render(request, "first_form.html", context=context)


def second_custom_form(request):
    if request.method == "POST":
        form = StuffForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("index")

        messages.error(request, "Invalid form data. Plz rewrite ")
        return redirect("form2")

    form = StuffForm()
    context = {"form": form}

    return render(request, "first_form.html", context=context)


def register_user(request):
    if request.method == "POST":
        form = RegisterUser(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
        else:
            return redirect("/register")

    form = RegisterUser()

    return render(request, "register.html", context={"form": form})

@login_required
def logout_user(request):
    logout(request)
    return redirect("/")