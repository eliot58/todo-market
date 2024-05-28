from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from core.models import *



@login_required(login_url="/login/")
def provider_profile(request):
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
        user.provider.site = request.POST['site']
        user.provider.description = request.POST['description']
        user.provider.save()
        return render(request, "provider_profile.html", {"regions": Region.objects.all(), "payments": PaymentMethod.objects.all(), "tags": Tag.objects.all(), "categories": Category.objects.all(), "stores": Store.objects.filter(provider=request.user.provider), "delivery_conditions": DeliveryCondition.objects.all(), 'products': Product.objects.filter(store__provider=request.user.provider), "success_save": True})
    return render(request, "provider_profile.html", {"regions": Region.objects.all(), "payments": PaymentMethod.objects.all(), "tags": Tag.objects.all(), "categories": Category.objects.all(), "stores": Store.objects.filter(provider=request.user.provider), "delivery_conditions": DeliveryCondition.objects.all(), 'products': Product.objects.filter(store__provider=request.user.provider)})


@login_required(login_url="/login/")
def buyer_profile(request):
    if request.method == "POST":
        user = request.user
        user.email = request.POST['email']
        user.buyer.phone = request.POST['phone']
        user.buyer.fullName = request.POST['fullName']
        user.save()
        user.buyer.save()
    return render(request, "buyer_profile.html")


@require_POST
@login_required(login_url="/login/")
def upload_files(request):
    for file in request.FILES.getlist("files"):
        ProviderFile.objects.create(provider=request.user.provider, file=file)
    return redirect(provider_profile)