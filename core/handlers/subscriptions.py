import json
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from core.models import *
import datetime
from django.utils import timezone
from aiogram import Bot
import asyncio
import uuid
from yookassa import Configuration, Payment


async def send_message(chat_id, text):
    bot = Bot(token=settings.BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=text)



@login_required(login_url="/login/")
def susbscriptions(request):
    if request.method == "POST":
        Configuration.account_id = settings.YOOKASSA_SHOP_ID
        Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

        base_url = "https://market.todotodo.ru" if not settings.DEBUG else "http://localhost:8000"

        if request.POST["application"] == "1":
            payment_response = Payment.create({
                "amount": {
                    "value": "3000.00",
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": base_url + "/susbscriptions/"
                },
                "capture": True,
                "description": "Оплата за услугу информационной подписки",
            }, uuid.uuid4())
            Application.objects.create(provider=request.user.provider, payment_id = payment_response.id)
            return JsonResponse({"confirmation_url": payment_response.confirmation._ConfirmationRedirect__confirmation_url})
        elif request.POST["application"] == "2":
            payment_response = Payment.create({
                "amount": {
                    "value": "10000.00",
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": base_url + "/susbscriptions/"
                },
                "capture": True,
                "description": "Оплата за услугу информационной подписки",
            }, uuid.uuid4())
            Application.objects.create(provider=request.user.provider, payment_id = payment_response.id)
            return JsonResponse({"confirmation_url": payment_response.confirmation._ConfirmationRedirect__confirmation_url})
        elif request.POST["application"] == "3":
            asyncio.run(send_message(222189723, f"Добавлено заявка на бегущую строку от {base_url}/admin/core/provider/{request.user.provider.id}/change/"))
        elif request.POST["application"] == "4":
            asyncio.run(send_message(222189723, f"Добавлено заявка на новость от {base_url}/admin/core/provider/{request.user.provider.id}/change/"))

        return JsonResponse({})
    return render(request, 'susbscriptions.html')


@csrf_exempt
def payment_webhook(request):
    if request.method == 'POST':
        event_json = json.loads(request.body)
        if 'event' in event_json and event_json['event'] == 'payment.succeeded':
            payment_id = event_json['object']['id']
            description = event_json['object']['description']
            application = get_object_or_404(Application, payment_id=payment_id)
            if application.checked != False:
                return HttpResponseForbidden()
            if description == "Магазин 3000":
                application.provider.status = "store"
                application.provider.status_time = timezone.now() + datetime.timedelta(days=30)
                application.provider.save()
            elif description == "Гипермаркет 10000":
                application.provider.status = "hyper"
                application.provider.status_time = timezone.now() + datetime.timedelta(days=30)
                application.provider.save()
            application.checked = True
            application.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'failed'})
    return JsonResponse({'status': 'invalid method'}, status=405)