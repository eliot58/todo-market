from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import *


def login_view(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd["username"], password=request.POST["password"])
            login(request, user)
            return redirect(index)
    else:
        login_form = LoginForm()
        register_form = RegisterForm()
    return render(request, "index.html", {"login_form": login_form, "register_form": register_form})



@require_POST
def signup(request):
    profile_form = RegisterForm(request.POST)
    if profile_form.is_valid():
        cd = profile_form.cleaned_data
        new_user = User()
        new_user.username = cd["email"]
        new_user.email = cd["email"]
        new_user.set_password(cd["password"])
        new_user.save()
        if cd["spec"] == "B":
            Buyer.objects.create(user=new_user)
        else:
            Provider.objects.create(user=new_user, email = cd["email"], phone = cd["phone"], fullName = cd["fullName"])

        user = authenticate(username=cd["email"], password=cd["password"])
        login(request, user)
    return redirect(index)

def logout_view(request):
    logout(request)
    return redirect(login_view)


@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")

def delivery(request):
    return render(request, "map.html")

def news(request):
    return render(request, "news.html", {"news": News.objects.all()})

def partner(request):
    return render(request, "partner.html")

def providers(request):
    return render(request, "providers.html")