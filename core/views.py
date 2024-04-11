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
import json
from django.core.serializers import serialize
from aiogram import Bot
from django.db import IntegrityError

bot = Bot(token=settings.BOT_TOKEN)


def login_view(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username = cd["username"], password = request.POST["password"])
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
            
            msg = "Вы зарегистрировались как " + spec + '\n' + "Ваш login: " + request.POST['email'] + '\n' + "Ваш password: " + password

            send_mail("Регистрация в todotodo", msg, settings.EMAIL_HOST_USER, [request.POST['email']], fail_silently = False)

            user = authenticate(username=cd["email"], password=password)
            login(request, user)
    else:
        return render(request, "index.html", {"login_form": LoginForm(), "register_form": RegisterForm()})
    return render(request, "index.html", {"login_form": LoginForm(), "register_form": register_form, "success_reg": True})

def logout_view(request):
    logout(request)
    return redirect(login_view)


@login_required(login_url="/login/")
def index(request):

    if request.GET.get("query", "") != "":
        try:
            Query.objects.create(user = request.user, query = request.GET["query"])
        except IntegrityError:
            pass

    providers = None
    flag = False
    if "query" in request.GET:
        flag = True
        tags = Tag.objects.filter(name__icontains = request.GET["query"])
        products = Product.objects.filter(name__icontains = request.GET["query"]).distinct()
        providers = {}
        for product in products.union(Product.objects.filter(tags__in = tags).distinct()):
            if product.store.provider.company not in providers:
                providers[product.store.provider.company] = {"provider_id": product.store.provider.id, "address": product.store.address, "products": [product], "logo": product.store.provider.logo.url}
            else:
                providers[product.store.provider.company]["products"].append(product)

        providers = providers.items()

    return render(request, "index.html", {"providers": providers, "stores": Store.objects.all(), "flag": flag})

def delivery(request):
    return render(request, "map.html", {"login_form": LoginForm(), "register_form": RegisterForm()})

def news(request):
    return render(request, "news.html", {"news": News.objects.all(), "login_form": LoginForm(), "register_form": RegisterForm()})

def partner(request):
    return render(request, "partner.html", {"login_form": LoginForm(), "register_form": RegisterForm()})

def providers(request):
    return render(request, "providers.html", {"providers": Provider.objects.all()[:6], "login_form": LoginForm(), "register_form": RegisterForm()})

def provider(request, id):
    items = {}
    for product in Product.objects.filter(store__provider_id=id):
        if product.category.name in items:
            items[product.category.name].append(product)
        else:
            items[product.category.name] = []
            items[product.category.name].append(product)
    return render(request, "provider.html", {"provider": Provider.objects.get(id=id), "products": items.items(), "login_form": LoginForm(), "register_form": RegisterForm()})

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
        return render(request, "profile.html", {"regions": Region.objects.all(),"payments": PaymentMethod.objects.all(), "tags": Tag.objects.all(), "categories": Category.objects.all(), "stores": Store.objects.filter(provider=request.user.provider), "delivery_conditions": DeliveryCondition.objects.all(), 'products': Product.objects.filter(store__provider=request.user.provider), "success_save": True})
    return render(request, "profile.html", {"regions": Region.objects.all(),"payments": PaymentMethod.objects.all(), "tags": Tag.objects.all(), "categories": Category.objects.all(), "stores": Store.objects.filter(provider=request.user.provider), "delivery_conditions": DeliveryCondition.objects.all(), 'products': Product.objects.filter(store__provider=request.user.provider)})

    
@login_required(login_url="/login/")
def buyer(request):
    if request.method == "POST":
        user = request.user
        user.email = request.POST['email']
        user.buyer.phone = request.POST['phone']
        user.buyer.fullName = request.POST['fullName']
        user.save()
        user.buyer.save()
    return render(request, "buyer.html")
    

@require_POST
def create_store(request):
    store = Store()
    store.provider = request.user.provider
    store.store_name = request.POST["store_name"]
    store.map_visor = request.POST["map_visor"]
    store.address = request.POST["address"]
    store.phone = request.POST["phone"]
    store.email = request.POST["email"]
    store.work_time_from = request.POST["work_time_from"]
    store.work_time_to = request.POST["work_time_to"]
    store.assembly_time = request.POST["assembly_time"]
    store.region_id = request.POST["region"]
    store.save()
    try:
        store.delivery_conditions.clear()
        for i in request.POST.getlist('delivery_conditions')[0].split(","):
            store.delivery_conditions.add(DeliveryCondition.objects.get(id=i))
    except KeyError:
        store.delivery_conditions.clear()
    try:
        store.payment_methods.clear()   
        for i in request.POST.getlist('payments')[0].split(","):
            store.payment_methods.add(PaymentMethod.objects.get(id=i))  
    except KeyError:
        store.payment_methods.clear() 
    # bot.send_message(chat_id=222189723, text = f"Создан магазин {request.POST['store_name']}")
    return redirect(profile)

@require_POST
def update_store(request, id):
    store = Store.objects.get(id=id)
    store.store_name = request.POST["store_name"]
    store.map_visor = request.POST["map_visor"]
    store.address = request.POST["address"]
    store.phone = request.POST["phone"]
    store.email = request.POST["email"]
    store.work_time_from = request.POST["work_time_from"]
    store.work_time_to = request.POST["work_time_to"]
    store.assembly_time = request.POST["assembly_time"]
    store.region_id = request.POST["region"]
    store.approve = False
    store.provider.save()
    store.save()
    try:
        store.delivery_conditions.clear()
        for i in request.POST.getlist('delivery_conditions')[0].split(","):
            store.delivery_conditions.add(DeliveryCondition.objects.get(id=i))
    except KeyError:
        store.delivery_conditions.clear()
    try:
        store.payment_methods.clear()   
        for i in request.POST.getlist('payments')[0].split(","):
            store.payment_methods.add(PaymentMethod.objects.get(id=i))  
    except KeyError:
        store.payment_methods.clear() 
    # bot.send_message(chat_id=222189723, text = f"Изменен магазин {request.POST['store_name']}")
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
    if request.user.provider.status == "free":
        if len(Product.objects.filter(store_id = request.POST["store"])) == 3:
            return JsonResponse({"status": "forbidden", "amount": 3})
    elif request.user.provider.status == "store":
        if len(Product.objects.filter(store_id = request.POST["store"])) == 10:
            return JsonResponse({"status": "forbidden", "amount": 10})
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
    for tag in request.POST["tags"].split():
        try:
            product.tags.add(Tag.objects.get(name = tag))
        except Tag.DoesNotExist:
            tag = Tag.objects.create(name = tag)
            product.tags.add(tag)
    return JsonResponse({"category": product.category.id, "articul": product.articul, "name": product.name, "image": product.image.url, "unit": product.unit, "remainder": product.remainder, "description": product.description, "id": product.id, "amount": product.amount, "price": product.price, "store": product.store.id, "tags": request.POST["tags"]})

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
        for tag in request.POST["tags"].split():
            try:
                product.tags.add(Tag.objects.get(name = tag))
            except Tag.DoesNotExist:
                tag = Tag.objects.create(name = tag)
                product.tags.add(tag)
    return JsonResponse({"category": product.category.id, "articul": product.articul, "name": product.name, "image": product.image.url, "unit": product.unit, "remainder": product.remainder, "description": product.description, "id": product.id, "amount": product.amount, "price": product.price, "store": product.store.id, "tags": request.POST["tags"]})

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
        ProviderFile.objects.create(provider = request.user.provider, file = file)
    return redirect(profile)

@login_required(login_url='/login/')
def cart(request):
    return render(request, 'cart.html', {'providers': request.user.buyer.cart.items()})

@require_POST
@csrf_exempt
@login_required(login_url='/login/')
def addtoCart(request, id):
    buyer = request.user.buyer
    item = Product.objects.get(id=id)
    if str(item.store.provider.id) in buyer.cart:
        if str(item.id) in buyer.cart[str(item.store.provider.id)]["items"]:
            buyer.cart[str(item.store.provider.id)]["items"][str(item.id)]['count'] += int(request.POST['count'])
            buyer.cart[str(item.store.provider.id)]["items"][str(item.id)]['all_price'] += item.price * int(request.POST['count'])
        else:
            buyer.cart[str(item.store.provider.id)]["items"][str(item.id)] = {
                'photo': item.image.url,
                'title': item.name + ", " + item.articul,
                'description': item.description,
                'price': item.price,
                'amount': item.amount,
                'unit': item.unit,
                'count': int(request.POST["count"]),
                'all_price': item.price * int(request.POST['count'])
            }
    else:
        buyer.cart[str(item.store.provider.id)] = {}
        buyer.cart[str(item.store.provider.id)]["address"] = item.store.address
        buyer.cart[str(item.store.provider.id)]["phone"] = item.store.phone
        buyer.cart[str(item.store.provider.id)]["site"] = item.store.provider.site
        buyer.cart[str(item.store.provider.id)]["photo"] = item.store.provider.logo.url
        buyer.cart[str(item.store.provider.id)]["region"] = item.store.region.name
        buyer.cart[str(item.store.provider.id)]["company"] = item.store.provider.company
        buyer.cart[str(item.store.provider.id)]["provider_id"] = item.store.provider.id
        buyer.cart[str(item.store.provider.id)]["store_id"] = item.store.id
        buyer.cart[str(item.store.provider.id)]["delivery_conditions"] = [{"id": delivery_condition.id, "name": delivery_condition.name} for delivery_condition in item.store.delivery_conditions.all()]
        buyer.cart[str(item.store.provider.id)]["items"] = {}
        buyer.cart[str(item.store.provider.id)]["items"][str(item.id)] = {
            'photo': item.image.url,
            'title': item.name + ", " + item.articul,
            'description': item.description,
            'price': item.price,
            'amount': item.amount,
            'unit': item.unit,
            'count': int(request.POST["count"]),
            'all_price': item.price * int(request.POST['count'])
        }
    buyer.total_price += item.price * int(request.POST['count'])
    buyer.save()
    return JsonResponse({"success": True})
    

@login_required(login_url='/login/')
def cart_item_delete(request, id):
    buyer = request.user.buyer
    item = Product.objects.get(id=id)
    buyer.total_price -= buyer.cart[str(item.store.provider.id)]["items"][str(item.id)]["all_price"]
    del buyer.cart[str(item.store.provider.id)]["items"][str(item.id)]
    if len(buyer.cart[str(item.store.provider.id)]["items"].items()) == 0:
        del buyer.cart[str(item.store.provider.id)]
    buyer.save()
    return redirect(cart)

@login_required(login_url='/login/')
@csrf_exempt
def cart_item_minus(request, id):
    buyer = request.user.buyer
    item = Product.objects.get(id=id)
    buyer.cart[str(item.store.provider.id)]["items"][str(item.id)]["all_price"] -= buyer.cart[str(item.store.provider.id)]["items"][str(item.id)]["price"]
    buyer.cart[str(item.store.provider.id)]["items"][str(item.id)]["count"] -= 1
    buyer.total_price -= buyer.cart[str(item.store.provider.id)]["items"][str(item.id)]["price"]
    buyer.save()
    return JsonResponse({"success": True})

@login_required(login_url='/login/')
@csrf_exempt
def cart_item_plus(request, id):
    buyer = request.user.buyer
    item = Product.objects.get(id=id)
    buyer.cart[str(item.store.provider.id)]["items"][str(item.id)]["all_price"] += buyer.cart[str(item.store.provider.id)]["items"][str(item.id)]["price"]
    buyer.cart[str(item.store.provider.id)]["items"][str(item.id)]["count"] += 1
    buyer.total_price += buyer.cart[str(item.store.provider.id)]["items"][str(item.id)]["price"]
    buyer.save()
    return JsonResponse({"success": True})

@login_required(login_url='/login/')
@csrf_exempt
def storeProducts(request, id):
    return JsonResponse({"store": serialize('json', Store.objects.filter(id = id)), "provider": serialize('json', [Store.objects.filter(id = id)[0].provider]), "products": serialize('json', Product.objects.filter(store_id = id))})


# @require_GET
# @csrf_exempt
# def search(request):
#     query = request.GET["query"]
#     tags = Tag.objects.filter(name__icontains = query)
#     products = Product.objects.filter(tags__in = tags)
#     return JsonResponse({"results": json.dumps(list(products.values("id", "name")))})

def susbscriptions(request):
    return render(request, "subs.html")

def orders(request):
    try:
        if request.user.provider:
            orders = Order.objects.filter(provider = request.user.provider)
    except:
        orders = Order.objects.filter(buyer = request.user.buyer)
    return render(request, 'orders.html', {"orders": orders})

def order(request, id):
    return render(request, 'order.html', {"order": Order.objects.get(id = id)})


def drawup(request):
    buyer = request.user.buyer
    provider = Provider.objects.get(id = id)
    order = Order()
    order.buyer = buyer
    order.provider = provider
    order.items = buyer.cart
    order.total_price = buyer.total_price
    order.delivery_id = request.POST["delivery"]
    if request.POST["delivery"] == "1":
        order.address = provider
    else:
        order.address = request.POST["address"]
    order.time = request.POST["time"]
    order.comment = request.POST["comment"]
    buyer.cart = {}
    buyer.total_price = 0
    buyer.save()
    return redirect(orders)