from django.shortcuts import render
from core.forms import *
from django.contrib.auth.decorators import login_required
from core.models import *
from django.db import IntegrityError



@login_required(login_url="/login/")
def index(request):
    if request.GET.get("query", "") != "":
        try:
            Query.objects.create(user=request.user, query=request.GET["query"])
        except IntegrityError:
            pass

    providers = None
    flag = False
    if "query" in request.GET:
        flag = True
        tags = Tag.objects.filter(name__icontains=request.GET["query"])
        products = Product.objects.filter(name__icontains=request.GET["query"]).distinct()
        providers = {}
        for product in products.union(Product.objects.filter(tags__in=tags).distinct()):
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


def markets(request):
    return render(request, "markets.html", {"markets": Store.objects.all()[:6], "login_form": LoginForm(), "register_form": RegisterForm()})


def market(request, id):
    return render(request, "market.html", {"market": Store.objects.get(id=id), "login_form": LoginForm(), "register_form": RegisterForm()})