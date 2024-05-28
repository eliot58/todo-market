from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings
from core.models import *
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist




@login_required(login_url="/login/")
def orders(request):
    try:
        orders = Order.objects.filter(provider=request.user.provider)
    except ObjectDoesNotExist:
        orders = Order.objects.filter(buyer=request.user.buyer)
    return render(request, 'orders.html', {"orders": orders})


@login_required(login_url="/login/")
def order(request, id):
    return render(request, 'order.html', {"order": Order.objects.get(id=id)})



@login_required(login_url="/login/")
def drawup(request, id):
    buyer = request.user.buyer
    provider = get_object_or_404(Provider, id=id)
    store = get_object_or_404(Store, id=buyer.cart[str(id)]["store_id"])
    order = Order.objects.create(
        buyer=buyer,
        provider=provider,
        store_id=store.id,
        items=buyer.cart[str(id)]["items"],
        total_price=sum(item["all_price"]
                        for item in buyer.cart[str(id)]["items"].values()),
        delivery=get_object_or_404(
            DeliveryCondition, name=request.POST["delivery"]),
        address=request.POST["address"] if request.POST["delivery"] != "Самовывоз" else store.address,
        time=request.POST["time"],
        delivery_date=request.POST["delivery_date"],
        comment=request.POST["comment"]
    )

    del buyer.cart[str(id)]
    buyer.total_price -= order.total_price
    buyer.save()

    base_url = "https://market.todotodo.ru" if not settings.DEBUG else "http://localhost:8000"

    send_mail(
        "Новый заказ",
        f"Новый заказ по адресу {base_url}/order/{order.id}/",
        settings.EMAIL_HOST_USER,
        [store.email],
        fail_silently=False
    )

    return redirect('orders')


@login_required(login_url="/login/")
def accept(request, id):
    order = get_object_or_404(Order, id=id)
    if order.provider.id != request.user.provider.id:
        return HttpResponseForbidden()

    order.accept = timezone.now()
    order.save()

    base_url = "https://market.todotodo.ru" if not settings.DEBUG else "http://localhost:8000"

    send_mail(
        f"Заказ #{order.id} принят",
        f"Заказ {base_url}/order/{order.id}/",
        settings.EMAIL_HOST_USER,
        [order.buyer.user.email],
        fail_silently=False
    )

    return redirect('order', id=order.id)


@login_required(login_url="/login/")
def transit(request, id):
    order = get_object_or_404(Order, id=id)
    if order.provider.id != request.user.provider.id:
        return HttpResponseForbidden()

    order.transit = timezone.now()
    order.save()

    base_url = "https://market.todotodo.ru" if not settings.DEBUG else "http://localhost:8000"

    send_mail(
        f"Заказ #{order.id} отгружен",
        f"Заказ {base_url}/order/{order.id}/",
        settings.EMAIL_HOST_USER,
        [order.buyer.user.email],
        fail_silently=False
    )

    return redirect('order', id=order.id)


@login_required(login_url="/login/")
def send_check(request, id):
    order = get_object_or_404(Order, id=id)
    if order.provider.id != request.user.provider.id:
        return HttpResponseForbidden()

    order.checkk = request.FILES["check"]
    order.check_date = timezone.now()
    order.save()

    base_url = "https://market.todotodo.ru" if not settings.DEBUG else "http://localhost:8000"

    send_mail(
        f"Получен счет для заказа #{order.id}",
        f"Получен счет для заказа {base_url}/order/{order.id}/",
        settings.EMAIL_HOST_USER,
        [order.buyer.user.email],
        fail_silently=False
    )

    return redirect('order', id=order.id)