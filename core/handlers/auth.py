from django.shortcuts import render, redirect
from core.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from core.models import *
from .common import index


def login_view(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(
                username=cd["username"], password=request.POST["password"])
            login(request, user)
            return redirect(index)
    else:
        return render(request, "index.html", {"login_form": LoginForm(), "register_form": RegisterForm()})
    return render(request, "index.html", {"login_form": login_form, "register_form": RegisterForm()})


@require_POST
def signup(request):
    if request.method == "POST":
        password = User.objects.make_random_password(length=8)
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            cd = register_form.cleaned_data
            new_user = User()
            new_user.username = cd["email"]
            new_user.email = cd["email"]
            new_user.set_password(password)
            new_user.save()
            spec = 'Покупатель' if request.POST['spec'] == 'B' else 'Поставщик'
            if cd["spec"] == "B":
                Buyer.objects.create(
                    user=new_user, phone=cd["phone"], fullName=cd["fullName"])
            else:
                Provider.objects.create(
                    user=new_user, email=cd["email"], phone=cd["phone"], fullName=cd["fullName"])

            msg = "Вы зарегистрировались как " + spec + '\n' + "Ваш login: " + \
                request.POST['email'] + '\n' + "Ваш password: " + password

            send_mail("Регистрация в todotodo", msg, settings.EMAIL_HOST_USER, [
                      request.POST['email']], fail_silently=False)

            user = authenticate(username=cd["email"], password=password)
            login(request, user)
    else:
        return render(request, "index.html", {"login_form": LoginForm(), "register_form": RegisterForm()})
    return render(request, "index.html", {"login_form": LoginForm(), "register_form": register_form, "success_reg": True})


def logout_view(request):
    logout(request)
    return redirect(login_view)