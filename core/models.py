from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


class Region(models.Model):
    name = models.CharField(max_length = 256, unique = True, verbose_name = "Название региона")

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length = 256, unique = True, verbose_name = "Название тэга")

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name
    
class DeliveryCondition(models.Model):
    name = models.CharField(max_length = 256, unique = True, verbose_name = "Условия доставки")

    class Meta:
        verbose_name = "Условия доставки"
        verbose_name_plural = "Условия доставки"

    def __str__(self):
        return self.name
    
class Ads(models.Model):
    img = models.ImageField(upload_to="ads", default = "ads/market.png", verbose_name="Фото")
    title = models.CharField(max_length = 256, default = "Todotodo Market", verbose_name="Заголовок")
    text = models.TextField(default = "Здесь может быть ваша релама",verbose_name="Текст")

    class Meta:
        verbose_name = "Бегущая строка"
        verbose_name_plural = "Бегущая строка"

    def __str__(self):
        return self.title

class Provider(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = "Аккаунт")
    logo = models.ImageField(upload_to="users/logo", null=True, blank=True)
    status_ch = [
        ("free", "Частник"),
        ("store", "Магазин"),
        ("hyper", "Гипермаркет")
    ]
    status = models.CharField(max_length = 256, choices = status_ch, default = "free", verbose_name = "Статус")
    company = models.CharField(max_length = 256, default = "", verbose_name = "Название компании")
    fullName = models.CharField(max_length = 256, verbose_name = "Контактное лицо")
    phone = models.CharField(max_length = 256, unique = True, verbose_name = "Номер телефона")
    email = models.EmailField(unique = True, verbose_name = "Email")
    slogan = models.CharField(max_length = 256, default = "", verbose_name = "Слоган")
    site = models.URLField(default = "", verbose_name = "Сайт")
    description = models.TextField(default = "", verbose_name = "Описание")


    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return self.fullName


class ProviderFile(models.Model):
    provider = models.ForeignKey(Provider, on_delete = models.CASCADE, verbose_name = "Поставщик")
    file = models.FileField(upload_to="users/file")


    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return self.provider.company


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = "Аккаунт")
    fullName = models.CharField(max_length = 256, verbose_name = "Контактное лицо")
    phone = models.CharField(max_length = 256, unique = True, verbose_name = "Номер телефона")
    cart = models.JSONField(default = dict(), blank = True)
    total_price = models.PositiveIntegerField(default=0)


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
    
class PaymentMethod(models.Model):
    name = models.CharField(max_length = 256, unique = True, verbose_name = "Способ оплаты")

    class Meta:
        verbose_name = "Способ оплаты"
        verbose_name_plural = "Способы оплаты"

    def __str__(self):
        return self.name
    

class Store(models.Model):
    provider = models.ForeignKey(Provider, on_delete = models.CASCADE, verbose_name = "Продавец")
    store_name = models.CharField(max_length = 256, verbose_name = "Название магазина")
    delivery_conditions = models.ManyToManyField(DeliveryCondition, verbose_name = "Условия доставки")
    payment_methods = models.ManyToManyField(PaymentMethod, verbose_name = "Способ оплаты")
    map_visor = models.CharField(max_length = 256, verbose_name = "Отображение на карте")
    contract = models.CharField(max_length = 256, null = True, blank = True, verbose_name = "Договор")
    address = models.CharField(max_length = 256, verbose_name = "Адрес склада для самовывоза")
    phone = models.CharField(max_length = 256, verbose_name = "Контакты для заказа")
    email = models.EmailField(verbose_name = "Email для выгрузок")
    work_time_from = models.TimeField(verbose_name = "Часы работы от")
    work_time_to = models.TimeField(verbose_name = "Часы работы до")
    region = models.ForeignKey(Region, on_delete = models.DO_NOTHING, verbose_name = "Регион")
    assembly_time = models.CharField(max_length = 256, verbose_name = "Время сборки")
    approve = models.BooleanField(default = False)


    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def __str__(self):
        return self.store_name
    
    def save(self):
        if self.approve == True:
            send_mail(f"Магазин {self.store_name}", f"Ваш магазин {self.store_name} прошел проверку", settings.EMAIL_HOST_USER, [self.email], fail_silently = False)

        super().save()

    
class Product(models.Model):
    store = models.ForeignKey(Store, on_delete = models.CASCADE, verbose_name = "Магазин")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name = "Категория")
    articul = models.CharField(max_length = 256, null = True, blank = True, verbose_name = "Артикул")
    name = models.CharField(max_length = 500, verbose_name = "Название товара")
    image = models.ImageField(upload_to="product", verbose_name="Фото")
    amount = models.PositiveIntegerField(verbose_name = "Количество")
    ch = [
        ("см", "см"),
        ("шт", "шт"),
        ("м2", "м2"),
    ]
    price = models.PositiveIntegerField(verbose_name = "Цена")
    unit = models.CharField(max_length = 10, choices = ch, verbose_name = "Ед. изм")
    remainder = models.PositiveIntegerField(verbose_name = "Остаток")
    description = models.TextField(null = True, blank = True, verbose_name = "Описание")
    tags = models.ManyToManyField(Tag)


    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name
    
class Query(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Аккаунт")
    query = models.TextField(unique = True)
    date = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = "Запрос"
        verbose_name_plural = "Запросы"

    def __str__(self):
        return self.query


class News(models.Model):
    logo = models.ImageField(upload_to="logo", verbose_name="Лого")
    author = models.CharField(max_length = 256, verbose_name = "Автор")
    text = models.TextField()


    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return str(self.id)
    

class Order(models.Model):
    provider = models.ForeignKey(Provider, on_delete = models.DO_NOTHING)
    buyer = models.ForeignKey(Buyer, on_delete = models.DO_NOTHING)
    store = models.ForeignKey(Store, on_delete = models.DO_NOTHING)
    status_ch = [
        ("work", "В работе"),
        ("accept", "Принят в работу"),
        ("transit", "В пути"),
        ("received", "Получен")
    ]
    status = models.CharField(max_length = 256, choices = status_ch, default = "work", verbose_name = "Статус")
    items = models.JSONField()
    checked = models.DateTimeField(null = True, blank = True)
    shipped_date = models.DateField(null = True, blank = True)
    delivery = models.ForeignKey(DeliveryCondition, on_delete = models.DO_NOTHING)
    address = models.CharField(max_length = 256, null = True, blank = True)
    time = models.TimeField()
    comment = models.TextField()
    total_price = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return str(self.id)