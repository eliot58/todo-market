import asyncio
from aiogram import Bot
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from core.models import *


async def send_message(chat_id, text):
    bot = Bot(token=settings.BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=text)

@require_POST
@csrf_exempt
@login_required(login_url="/login/")
def create_product(request):
    base_url = "https://market.todotodo.ru" if not settings.DEBUG else "http://localhost:8000"
    store = Store.objects.get(id=request.POST["store"])
    if store.provider != request.user.provider:
        return HttpResponseForbidden()
    product = Product()
    product.store = store
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
    for tag in request.POST["tags"].split(", "):
        try:
            product.tags.add(Tag.objects.get(name=tag))
        except Tag.DoesNotExist:
            tag = Tag.objects.create(name=tag)
            product.tags.add(tag)

    asyncio.run(send_message(
        -4231343211, f"Создан товар {product.name}\nДля магазина {base_url}/admin/core/store/{store.id}/change/"))
    
    return JsonResponse({"category": product.category.id, "articul": product.articul, "name": product.name, "image": product.image.url, "unit": product.unit, "remainder": product.remainder, "description": product.description, "id": product.id, "amount": product.amount, "price": product.price, "store": product.store.id, "tags": request.POST["tags"]})


@require_POST
@csrf_exempt
@login_required(login_url="/login/")
def update_product(request, id):
    base_url = "https://market.todotodo.ru" if not settings.DEBUG else "http://localhost:8000"
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
        for tag in request.POST["tags"].split(", "):
            try:
                product.tags.add(Tag.objects.get(name=tag))
            except Tag.DoesNotExist:
                tag = Tag.objects.create(name=tag)
                product.tags.add(tag)

    asyncio.run(send_message(
        -4231343211, f"Изменен товар {product.name}\nВ магазине {base_url}/admin/core/store/{product.store.id}/change/"))
    
    return JsonResponse({"category": product.category.id, "articul": product.articul, "name": product.name, "image": product.image.url, "unit": product.unit, "remainder": product.remainder, "description": product.description, "id": product.id, "amount": product.amount, "price": product.price, "store": product.store.id, "tags": request.POST["tags"]})


@require_GET
@csrf_exempt
@login_required(login_url="/login/")
def delete_product(request, id):
    product = Product.objects.get(id=id)
    if request.user.provider == product.store.provider:
        product.delete()
    return HttpResponse(id)


@csrf_exempt
@login_required(login_url="/login/")
def check_status(request):
    if request.user.provider.status == "free":
        if len(Product.objects.filter(store_id=request.POST["store"])) == 3:
            return JsonResponse({"status": "forbidden", "amount": 3})
    elif request.user.provider.status == "store":
        if len(Product.objects.filter(store_id=request.POST["store"])) == 10:
            return JsonResponse({"status": "forbidden", "amount": 10})
        
    return JsonResponse({})
        
    