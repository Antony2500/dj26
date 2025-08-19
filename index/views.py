import datetime
from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordResetForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .forms import RenewBookForm, StuffForm, RegisterUser, BookForm, BookForm2
from .models import Stuff, Book, Article

def index(request):
    if 'counter' in request.COOKIES:
        ent = int(request.COOKIES['counter']) + 1
    else:
        ent = 1
    print(request.session)
    response = render(request, "index.html", context={"title": "Main"})
    response.set_cookie(
        "counter",  # Назва cookie
        ent,  # Значення cookie
        max_age=None,  # Час життя в секундах
        expires=None,  # Дата/час, коли cookie стане неактивним
        path='/',  # Шлях, на якому cookie буде доступне
        domain=None,  # Домен, на якому cookie буде доступне
        secure=False,  # Чи надсилати cookie лише через HTTPS
        httponly=False,  # Чи доступне cookie лише через HTTP (не JS)
    )
    if request.session:
        print(request.session.session_key)
        request.session.set_expiry(300)
        request.session.get_expiry_date() # get_expiry_age
    return response

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


def get_all_stuff2(request):
    all_stuff = Stuff.objects.all()
    paginator = Paginator(all_stuff, 2)

    if "page" in request.GET:
        page_num = request.GET.get("page", 1)
    else:
        page_num = 1

    page = paginator.get_page(page_num)
    return render(request, "stuff.html", {"page": page, "stuffs": page.object_list})


def create_new_product(request):
    if request.method == "POST":
        pass

    form = BookForm()

    return render(request, "new_form.html", {"form": form})


def book_edit_view(request):
    BookFormSet = modelformset_factory(Book, BookForm2, extra=0)

    if request.method == "POST":
        formset = BookFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("book_formset")

    formset = BookFormSet(queryset=Book.objects.all())

    return render(request, "formset.html", {"formset": formset})


def create_book_view_set(request):
    BookFormSet = modelformset_factory(Book, BookForm2, extra=3)

    if request.method == "POST":
        formset = BookFormSet(request.POST, queryset=Book.objects.none())
        if formset.is_valid():
            formset.save()
            return redirect("create_book_formset")

    formset = BookFormSet(queryset=Book.objects.none())

    return render(request, "formset.html", {"formset": formset})


def my_view(request):
    messages.debug(request, 'This is a debug message.')
    messages.info(request, 'This is an informational message.')
    messages.success(request, 'This is a success message.')
    messages.warning(request, 'This is a warning message.')
    messages.error(request, 'This is an error message.')
    return render(request, 'my_template.html')

def test_signal(request):
    user = User.objects.create_user(username='tony', password='secret')
    return HttpResponse(f"{user}")


def create_article(request):
    article = Article(
        title="AI caan provid,,,e ,  ...new opport.uni.ty   ! to  treat all cancer problems  ! ",
        content="huf92gbu-y9fb-y92fby92by92b8y-cbu8ydfb28yubde2hubehu2uhnd2uhndub-2ub-hn92fubn",
    )
    article.save()
    return HttpResponse(f"{article}")


def send_mail_console(request):
    response = send_mail(
        subject="Registration email",
        message="Дякуємо, що зареєструвались\n ",
        from_email=None,
        recipient_list=['anton.andreiev2003@gmail.com'],
        fail_silently=False,
        html_message="""<h2 style="color:#2c7be5">Вітаємо у сервісі!</h2>
        <p>Дякуємо, що <b>зареєструвались</b>.</p>
        <a href="http://127.0.0.1:8000/" style="padding:8px 16px;
           background:#2c7be5;color:#fff;text-decoration:none;border-radius:4px">
           Перейти на сайт
        </a>
        """
    )
    return HttpResponse(f"{response}")


def bad_request(request):
    return render(request, "400.html")


def reset_password(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            user_from_form = User.objects.filter(Q(email=data))
            if user_from_form.exists():
                for user in user_from_form:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, None, [user.email], fail_silently=False)
                    except Exception as e:
                        print(e)
                        return redirect("400_bad_request")
                    return redirect("accounts/password_reset/done/")

        return redirect("400_bad_request")

    password_reset_form = PasswordResetForm()
    return render(
        request,
        "registration/password_reset.html",
        context={"password_reset_form": password_reset_form}
    )

from django.core.cache import cache
from django.views.decorators.cache import cache_page

def example_expensive_operation(request):
    result = cache.get("result")
    if result is None:
        result = sum(i * i for i in range(10000000))
        cache.set("result", result, timeout=10)
    return HttpResponse(f"{result}")


@cache_page(60)
def my_cache(request):
    data = sum(i * i for i in range(10000000))
    return render(request, "cache_template.html", {"cache_data": data})