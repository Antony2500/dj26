from django.shortcuts import render



def index(request):
    return render(request, "index.html", context={"title": "Main"})

def test_login(request):
    return render(request, "test_login.html", context={"title": "Main"})