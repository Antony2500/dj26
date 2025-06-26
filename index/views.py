import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.urls import reverse

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
            return redirect("index")
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


def request_info_check(request):
    info = []

    # Основні атрибути
    info.append(f"Method: {request.method}")
    info.append(f"Scheme: {request.scheme}")
    info.append(f"Path: {request.path}")
    info.append(f"Encoding: {request.encoding}")
    info.append(f"Content-Type: {request.content_type}")
    info.append(f"Content Params: {request.content_params}")
    # GET і POST параметри
    info.append(f"GET params: {dict(request.GET)}")
    info.append(f"POST params: {dict(request.POST)}")

    # Файли
    info.append(f"FILES: {[f.name for f in request.FILES.values()]}")

    # META-поля (тільки кілька, бо їх дуже багато)
    meta_keys = [
        'CONTENT_LENGTH', 'CONTENT_TYPE', 'HTTP_USER_AGENT',
        'HTTP_ACCEPT', 'HTTP_HOST', 'HTTP_REFERER',
        'REMOTE_ADDR', 'REMOTE_HOST', 'REMOTE_USER',
        'QUERY_STRING', 'SERVER_NAME', 'REQUEST_METHOD'
    ]
    for key in meta_keys:
        info.append(f"META[{key}]: {request.META.get(key)}")

    # resolver_match
    info.append(f"Resolver match: {request.resolver_match}")

    # Заголовки (Django 2.2+)
    if hasattr(request, 'headers'):
        headers = '\n'.join([f"{k}: {v}" for k, v in request.headers.items()])
        info.append("Headers:\n" + headers)

    # Додаткові методи
    info.append(f"Host: {request.get_host()}")
    info.append(f"Port: {request.get_port()}")
    info.append(f"Full Path: {request.get_full_path()}")
    info.append(f"Absolute URL: {request.build_absolute_uri()}")
    info.append(f"Is secure: {request.is_secure()}")

    # AJAX-перевірка
    if hasattr(request, 'is_ajax'):  # Застаріле, але покажемо
        info.append(f"Is AJAX: {request.is_ajax()}")

    return HttpResponse("<br>".join(info), content_type="text/html")

def redirect_view(request, pk: int, stuff_name: str):
    stuff = get_object_or_404(Stuff, pk=pk, stuff_name=stuff_name)

    if not stuff:
       return HttpResponse("404 NOT found")

    url = reverse("info_stuff", kwargs={"pk": pk})
    return redirect(url)

def info_view(request, pk: int, stuff_name: str):
    stuff = get_object_or_404(Stuff, pk=pk, stuff_name=stuff_name)
    return HttpResponse(f"Information about Stuff {pk} and {stuff_name} - {stuff.__dict__}")


from django.views.generic import TemplateView, ListView

class AboutUs(TemplateView):
    template_name = "test_login.html"


class StuffListView(ListView):
    model = Stuff

    def get(self, *args, **kwargs):
        pass

