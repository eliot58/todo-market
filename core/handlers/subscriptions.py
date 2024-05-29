import json
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from core.models import *
import datetime
from django.utils import timezone
import uuid
from yookassa import Configuration, Payment




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
            ProviderOrder.objects.create(provider=request.user.provider, type="status", payment_id = payment_response.id, status = "store")
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
            ProviderOrder.objects.create(provider=request.user.provider, type="status", payment_id = payment_response.id, status = "hyper")
            return JsonResponse({"confirmation_url": payment_response.confirmation.confirmation_url})
        elif request.POST["application"] == "3":
            payment_response = Payment.create({
                "amount": {
                    "value": str(float(request.POST["days"]) * 1000),
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": base_url + "/susbscriptions/"
                },
                "capture": True,
                "description": "Оплата за услугу информационной подписки",
            }, uuid.uuid4())
            ProviderOrder.objects.create(provider=request.user.provider, type="ticker", payment_id = payment_response.id, ticker = request.POST["ticker"], ticker_days = request.POST["days"])
            return JsonResponse({"confirmation_url": payment_response.confirmation.confirmation_url})
        elif request.POST["application"] == "4":
            payment_response = Payment.create({
                "amount": {
                    "value": "5000.00",
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": base_url + "/susbscriptions/"
                },
                "capture": True,
                "description": "Оплата за услугу информационной подписки",
            }, uuid.uuid4())
            ProviderOrder.objects.create(provider=request.user.provider, type="news", payment_id = payment_response.id, news = request.POST["news"])
            return JsonResponse({"confirmation_url": payment_response.confirmation.confirmation_url})

    return render(request, 'susbscriptions.html')


@csrf_exempt
def payment_webhook(request):
    if request.method == 'POST':
        event_json = json.loads(request.body)
        if 'event' in event_json and event_json['event'] == 'payment.succeeded':
            payment_id = event_json['object']['id']
            order = get_object_or_404(ProviderOrder, payment_id=payment_id)
            if order.paid != False:
                return HttpResponseForbidden()
            if order.type == "status":
                order.provider.status = order.status
                order.provider.status_time = timezone.now() + datetime.timedelta(days=30)
                order.provider.save()
            elif order.type == "ticker":
                Ticker.objects.create(provider=order.provider, text=order.ticker, visible_date=timezone.now() + datetime.timedelta(days=order.ticker_days))
            elif order.type == "news":
                News.objects.create(provider=order.provider, text=order.news)
            order.paid = True
            order.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'failed'})
    return JsonResponse({'status': 'invalid method'}, status=405)