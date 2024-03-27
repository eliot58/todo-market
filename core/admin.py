from django.contrib import admin
from .models import *
from django.forms import CheckboxSelectMultiple

class ProviderFileInline(admin.StackedInline):
    model = ProviderFile
    extra = 0

class StoreInline(admin.StackedInline):
    model = Store
    extra = 0

class ProductInline(admin.StackedInline):
    model = Product
    extra = 0

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    inlines = [ProviderFileInline, StoreInline]
    list_display = ['user', 'company', 'fullName', 'phone', 'email']

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['user', 'fullName', 'phone']

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    inlines = [ProductInline]
    list_display = ['provider', 'store_name', 'address', 'phone', 'email']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['author', 'text']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(DeliveryCondition)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ['user', "query", "date"]


admin.site.register(Ads)