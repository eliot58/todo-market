from aiogram import Bot
from django.http import JsonResponse
from django.shortcuts import redirect
from core.forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from core.models import *
import asyncio
from .profile import provider_profile
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt

async def send_message(chat_id, text):
    bot = Bot(token=settings.BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=text)

@require_POST
@login_required(login_url="/login/")
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

    asyncio.run(send_message(
        222189723, f"Создан магазин {request.POST['store_name']}"))

    return redirect(provider_profile)


@require_POST
@login_required(login_url="/login/")
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

    asyncio.run(send_message(
        "222189723", f"Изменен магазин {request.POST['store_name']}"))
    return redirect(provider_profile)


@require_GET
@login_required(login_url="/login/")
def delete_store(request, id):
    store = Store.objects.get(id=id)
    if request.user.provider == store.provider:
        store.delete()
    return redirect(provider_profile)


@login_required(login_url='/login/')
@csrf_exempt
def storeProducts(request, id):
    return JsonResponse({"store": serialize('json', Store.objects.filter(id=id)), "provider": serialize('json', [Store.objects.filter(id=id)[0].provider]), "products": serialize('json', Product.objects.filter(store_id=id))})