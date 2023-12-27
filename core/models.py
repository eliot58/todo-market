from django.db import models
from django.contrib.auth.models import User


class Region(models.Model):
    name = models.CharField(max_length = 256, unique = True, verbose_name = "Название региона")

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

    def __str__(self):
        return self.name
    
class DeliveryCondition(models.Model):
    name = models.CharField(max_length = 256, unique = True, verbose_name = "Условия доставки")

    class Meta:
        verbose_name = "Условия доставки"
        verbose_name_plural = "Условия доставки"

    def __str__(self):
        return self.name

class Provider(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = "Аккаунт")
    logo = models.ImageField(upload_to="users/logo", null=True, blank=True)
    company = models.CharField(max_length = 256, verbose_name = "Название компании", null = True, blank = True)
    fullName = models.CharField(max_length = 256, verbose_name = "Контактное лицо")
    phone = models.CharField(max_length = 256, unique = True, verbose_name = "Номер телефона")
    email = models.EmailField(unique = True, verbose_name = "Email")
    region = models.ForeignKey(Region, on_delete = models.CASCADE, verbose_name = "Регион", null = True, blank = True)


    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return self.company


class ProviderFile(models.Model):
    provider = models.ForeignKey(Provider, on_delete = models.CASCADE, verbose_name = "Поставщик")
    file = models.FileField(upload_to="users/file")


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = "Аккаунт")
    fullName = models.CharField(max_length = 256, verbose_name = "Контактное лицо")
    phone = models.CharField(max_length = 256, unique = True, verbose_name = "Номер телефона")
    cart = models.JSONField(default = dict(), blank = True)


    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"


class Category(models.Model):
    name = models.CharField(max_length = 256, unique = True, verbose_name = "Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
    

class Store(models.Model):
    provider = models.ForeignKey(Provider, on_delete = models.CASCADE, verbose_name = "Продавец")
    manager = models.CharField(max_length = 256, verbose_name = "Менеджер")
    delivery_condition = models.CharField(max_length = 256, verbose_name = "Условия доставки")
    map_visor = models.CharField(max_length = 256, verbose_name = "Отображение на карте")
    contract = models.CharField(max_length = 256, null = True, blank = True, verbose_name = "Договор")
    site = models.URLField(verbose_name = "Сайт")
    address = models.CharField(max_length = 256, verbose_name = "Адрес склада для самовывоза")
    phone = models.CharField(max_length = 256, verbose_name = "Контакты для заказа")
    slogan = models.CharField(max_length = 256, verbose_name = "Слоган")
    email = models.EmailField(verbose_name = "Email для выгрузок")
    work_time = models.CharField(max_length = 256, verbose_name = "Часы работы")
    assembly_time = models.CharField(max_length = 256, verbose_name = "Время сборки")
    description = models.TextField(verbose_name = "Описание")


    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def __str__(self):
        return self.manager

    
class Product(models.Model):
    store = models.ForeignKey(Store, on_delete = models.CASCADE, verbose_name = "Магазин")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name = "Категория")
    articul = models.CharField(max_length = 256, null = True, blank = True, verbose_name = "Артикул")
    name = models.CharField(max_length = 256, verbose_name = "Название товара")
    image = models.ImageField(upload_to="product", verbose_name="Фото")
    amount = models.PositiveIntegerField(verbose_name = "Количество")
    ch = [
        ("см", "см"),
        ("шт", "шт"),
        ("м2", "м2"),
    ]
    unit = models.CharField(max_length = 10, choices = ch, verbose_name = "Ед. изм")
    remainder = models.PositiveIntegerField(verbose_name = "Остаток")
    description = models.TextField(null = True, blank = True, verbose_name = "Описание")


    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class News(models.Model):
    logo = models.ImageField(upload_to="logo", verbose_name="Лого")
    author = models.CharField(max_length = 256, verbose_name = "Автор")
    text = models.TextField()


    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return str(self.id)
    

class Work(models.Model):
    pass