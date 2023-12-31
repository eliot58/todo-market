from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from .utils import generator


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
        password = generator(8)
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            cd = register_form.cleaned_data
            new_user = User()
            new_user.username = cd["email"]
            new_user.email = cd["email"]
            new_user.set_password(password)
            new_user.save()
            spec = 'Покупатель' if request.POST['spec']=='B' else 'Поставщик'
            if cd["spec"] == "B":
                Buyer.objects.create(user=new_user, phone = cd["phone"], fullName = cd["fullName"])
            else:
                Provider.objects.create(user=new_user, email = cd["email"], phone = cd["phone"], fullName = cd["fullName"])
            
            msg = 'Вы зарегистрировались как ' + spec + '\n' + 'Ваш login: ' + request.POST['email'] + '\n' + 'Ваш password: ' + password

            print(password)

            # send_mail('Регистрация в todotodo', msg, settings.EMAIL_HOST_USER, [request.POST['email']], fail_silently=False)

            user = authenticate(username=cd["email"], password=password)
            login(request, user)
    else:
        return render(request, "index.html", {"login_form": LoginForm(), "register_form": RegisterForm()})
    return render(request, "index.html", {"login_form": LoginForm(), "register_form": register_form})

def logout_view(request):
    logout(request)
    return redirect(login_view)

# u7HsMJ4A

@login_required(login_url="/login/")
def index(request):
    products = Product.objects.filter(name__icontains=request.GET.get("key", "")) & Product.objects.filter(price__range=(request.GET.get("price_from", 1), request.GET.get("price_to", 1000000)))
    return render(request, "index.html", {"regions": Region.objects.all(), "categories": Category.objects.all(), "stores": Store.objects.all(), "products": products})

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
        try:
            user.provider.logo = request.FILES['logo']
        except KeyError:
            pass
        user.provider.slogan = request.POST['slogan']
        user.provider.site = request.POST['site']
        user.provider.description = request.POST['description']
        user.provider.save()
        return redirect(profile)
    print(type(request.user.provider.logo))
    return render(request, "profile.html", {"regions": Region.objects.all(), "categories": Category.objects.all(), "stores": Store.objects.filter(provider=request.user.provider), "delivery_conditions": DeliveryCondition.objects.all(), 'products': Product.objects.filter(store__provider=request.user.provider)})

@require_POST
def create_store(request):
    store = Store()
    store.provider = request.user.provider
    store.manager = request.POST["manager"]
    store.delivery_condition_id = request.POST["delivery_condition"]
    store.map_visor = request.POST["map_visor"]
    store.address = request.POST["address"]
    store.phone = request.POST["phone"]
    store.email = request.POST["email"]
    store.work_time = request.POST["work_time"]
    store.assembly_time = request.POST["assembly_time"]
    store.region_id = request.POST["region"]
    store.save()
    return redirect(profile)

@require_POST
def update_store(request, id):
    store = Store.objects.get(id=id)
    store.manager = request.POST["manager"]
    store.delivery_condition_id = request.POST["delivery_condition"]
    store.map_visor = request.POST["map_visor"]
    store.address = request.POST["address"]
    store.phone = request.POST["phone"]
    store.email = request.POST["email"]
    store.work_time = request.POST["work_time"]
    store.assembly_time = request.POST["assembly_time"]
    store.region_id = request.POST["region"]
    store.save()
    return redirect(profile)

@require_GET
def delete_store(request, id):
    store = Store.objects.get(id=id)
    if request.user.provider == store.provider:
        store.delete()
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
    product.price = request.POST["price"]
    product.remainder = request.POST["remainder"]
    product.description = request.POST["description"]
    product.save()
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
        product.price = request.POST["price"]
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
    for file in request.FILES.getlist("files"):
        ProviderFile.objects.create(provider=request.user.provider, file = file)
    return redirect(profile)
