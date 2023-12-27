from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
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
        return render(request, "index.html", {"login_form": LoginForm(), "register_form": RegisterForm()})
    return render(request, "index.html", {"login_form": login_form, "register_form": RegisterForm()})



@require_POST
def signup(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            cd = register_form.cleaned_data
            new_user = User()
            new_user.username = cd["email"]
            new_user.email = cd["email"]
            new_user.set_password(cd["password"])
            new_user.save()
            if cd["spec"] == "B":
                Buyer.objects.create(user=new_user, phone = cd["phone"], fullName = cd["fullName"])
            else:
                Provider.objects.create(user=new_user, email = cd["email"], phone = cd["phone"], fullName = cd["fullName"])

            user = authenticate(username=cd["email"], password=cd["password"])
            login(request, user)
    else:
        return render(request, "index.html", {"login_form": LoginForm(), "register_form": RegisterForm()})
    return render(request, "index.html", {"login_form": LoginForm(), "register_form": register_form})

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
    return render(request, "providers.html", {"providers": Provider.objects.all()[:6]})

def provider(request, id):
    return render(request, "provider.html", {"provider": Provider.objects.get(id=id)})

@login_required(login_url="/login/")
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.provider.fullName = request.POST['fullName']
        user.provider.phone = request.POST['phone']
        user.provider.email = request.POST['email']
        user.provider.company = request.POST['company']
        user.provider.logo = request.FILES['logo']
        user.provider.region_id = request.POST['region']
        user.provider.save()
        return redirect(profile)
    return render(request, "profile.html", {"regions": Region.objects.all(), "categories": Category.objects.all(), "stores": Store.objects.filter(provider=request.user.provider), "delivery_conditions": DeliveryCondition.objects.all(), 'products': Product.objects.filter(store__provider=request.user.provider)})

@require_POST
def create_store(request):
    store = Store()
    store.provider = request.user.provider
    store.manager = request.POST["manager"]
    store.delivery_condition = request.POST["delivery_condition"]
    store.map_visor = request.POST["map_visor"]
    store.site = request.POST["site"]
    store.address = request.POST["address"]
    store.phone = request.POST["phone"]
    store.slogan = request.POST["slogan"]
    store.email = request.POST["email"]
    store.work_time = request.POST["work_time"]
    store.assembly_time = request.POST["assembly_time"]
    store.description = request.POST["description"]
    store.save()
    return redirect(profile)


@require_POST
@csrf_exempt
def create_product(request):
    product = Product()
    product.store_id = request.POST["store"]
    product.category_id = request.POST["category"]
    product.articul = request.POST["articul"]
    product.name = request.POST["name"]
    product.image = request.FILES['photo']
    product.unit = request.POST["unit"]
    product.amount = request.POST["amount"]
    product.remainder = request.POST["remainder"]
    product.description = request.POST["description"]
    product.save()
    print(product.image.url)
    return JsonResponse({"category": product.category.id, "articul": product.articul, "name": product.name, "image": product.image.url, "unit": product.unit, "remainder": product.remainder, "description": product.description, "id": product.id, "amount": product.amount})

@require_POST
@csrf_exempt
def update_product(request, id):
    product = Product.objects.get(id=id)
    if request.user.provider == product.store.provider:
        product.articul = request.POST["articul"]
        product.name = request.POST["name"]
        product.amount = request.POST["amount"]
        try:
            product.image = request.FILES['photo']
        except KeyError:
            pass
        product.unit = request.POST["unit"]
        product.remainder = request.POST["remainder"]
        product.description = request.POST["description"]
        product.save()
    return JsonResponse({"category": product.category.id, "articul": product.articul, "name": product.name, "image": product.image.url, "unit": product.unit, "remainder": product.remainder, "description": product.description, "id": product.id, "amount": product.amount})

@require_GET
@csrf_exempt
def delete_product(request, id):
    product = Product.objects.get(id=id)
    if request.user.provider == product.store.provider:
        product.delete()
    return HttpResponse(id)

@require_POST
def upload_files(request):
    pass