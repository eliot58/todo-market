from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from core.models import *




@require_POST
@csrf_exempt
@login_required(login_url="/login/")
def create_product(request):
    if request.user.provider.status == "free":
        if len(Product.objects.filter(store_id=request.POST["store"])) == 3:
            return JsonResponse({"status": "forbidden", "amount": 3})
    elif request.user.provider.status == "store":
        if len(Product.objects.filter(store_id=request.POST["store"])) == 10:
            return JsonResponse({"status": "forbidden", "amount": 10})
    store = Store.objects.get(id=request.POST["store"])
    store.approve = False
    store.save()
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
    return JsonResponse({"category": product.category.id, "articul": product.articul, "name": product.name, "image": product.image.url, "unit": product.unit, "remainder": product.remainder, "description": product.description, "id": product.id, "amount": product.amount, "price": product.price, "store": product.store.id, "tags": request.POST["tags"]})


@require_POST
@csrf_exempt
@login_required(login_url="/login/")
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
        product.store.approve = False
        product.store.save()
        for tag in request.POST["tags"].split(", "):
            try:
                product.tags.add(Tag.objects.get(name=tag))
            except Tag.DoesNotExist:
                tag = Tag.objects.create(name=tag)
                product.tags.add(tag)
    return JsonResponse({"category": product.category.id, "articul": product.articul, "name": product.name, "image": product.image.url, "unit": product.unit, "remainder": product.remainder, "description": product.description, "id": product.id, "amount": product.amount, "price": product.price, "store": product.store.id, "tags": request.POST["tags"]})


@require_GET
@csrf_exempt
@login_required(login_url="/login/")
def delete_product(request, id):
    product = Product.objects.get(id=id)
    if request.user.provider == product.store.provider:
        product.delete()
    return HttpResponse(id)