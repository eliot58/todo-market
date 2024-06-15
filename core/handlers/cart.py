from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from core.models import *


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
            buyer.cart[str(item.store.provider.id)]["items"][str(
                item.id)]['count'] += int(request.POST['count'])
            buyer.cart[str(item.store.provider.id)]["items"][str(
                item.id)]['all_price'] += item.price * int(request.POST['count'])
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
        buyer.cart[str(item.store.provider.id)
                   ]["site"] = item.store.provider.site
        buyer.cart[str(item.store.provider.id)
                   ]["photo"] = item.store.provider.logo.url
        buyer.cart[str(item.store.provider.id)
                   ]["region"] = item.store.region.name
        buyer.cart[str(item.store.provider.id)
                   ]["company"] = item.store.store_name
        buyer.cart[str(item.store.provider.id)]["store_id"] = item.store.id
        buyer.cart[str(item.store.provider.id)]["delivery_conditions"] = [
            {"id": delivery_condition.id, "name": delivery_condition.name} for delivery_condition in item.store.delivery_conditions.all()]
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
@login_required(login_url="/login/")
def cart_item_delete(request, id):
    buyer = request.user.buyer
    item = Product.objects.get(id=id)
    buyer.total_price -= buyer.cart[str(item.store.provider.id)
                                    ]["items"][str(item.id)]["all_price"]
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
    buyer.cart[str(item.store.provider.id)]["items"][str(
        item.id)]["all_price"] -= buyer.cart[str(item.store.provider.id)]["items"][str(item.id)]["price"]
    buyer.cart[str(item.store.provider.id)
               ]["items"][str(item.id)]["count"] -= 1
    buyer.total_price -= buyer.cart[str(item.store.provider.id)
                                    ]["items"][str(item.id)]["price"]
    buyer.save()
    return JsonResponse({"success": True})


@login_required(login_url='/login/')
@csrf_exempt
def cart_item_plus(request, id):
    buyer = request.user.buyer
    item = Product.objects.get(id=id)
    buyer.cart[str(item.store.provider.id)]["items"][str(
        item.id)]["all_price"] += buyer.cart[str(item.store.provider.id)]["items"][str(item.id)]["price"]
    buyer.cart[str(item.store.provider.id)
               ]["items"][str(item.id)]["count"] += 1
    buyer.total_price += buyer.cart[str(item.store.provider.id)
                                    ]["items"][str(item.id)]["price"]
    buyer.save()
    return JsonResponse({"success": True})