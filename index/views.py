import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages

from .forms import RenewBookForm, StuffForm, RegisterUser
from .models import Stuff

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

@login_required
def get_stuff(request, id_: int):
    stuff = Stuff.objects.get(pk=id_)
    print(stuff)
    return HttpResponse(f"{[stuff.pk, stuff.stuff_name, stuff.stuff_desc, stuff.price, stuff.photo]}")

def get_all_stuff(request):
    all_stuff = Stuff.objects.all()
    print(type(all_stuff))
    return HttpResponse(all_stuff)

def create_stuff(request):
    new_stuff = Stuff(
        stuff_name="Book",
        stuff_desc="Tralelo Tralala",
        photo="",
        price=15151
    )

    new_stuff.save()
    return HttpResponse("Work")

def get_or_create_stuff(request, id_: int):
    stuff = Stuff.objects.get_or_create(pk=id_, defaults={"price": 1})
    return HttpResponse(stuff)

def update_stuff(request, id_: int):
    stuff = get_object_or_404(Stuff, pk=id_)

    stuff.stuff_name = "Optimus Prime"
    stuff.save()

    return HttpResponse(stuff)

def delete_stuff(request, id_: int):
    stuff = get_object_or_404(Stuff, pk=id_)

    stuff.delete()
    stuff.save()

    return HttpResponse(stuff)