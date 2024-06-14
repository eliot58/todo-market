from django.shortcuts import get_object_or_404
from rest_framework import generics
from core.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Count

class RegionViewSet(generics.ListAPIView):
    serializer_class = RegionSerializer

    def get_queryset(self, *args, **kwargs):
        id = self.request.query_params.get('id')
        if id is not None:
            data = Region.objects.filter(id=id)
        else:
            data = Region.objects.all()
        return data
    

class TagViewSet(generics.ListAPIView):
    serializer_class = TagSerializer

    def get_queryset(self, *args, **kwargs):
        id = self.request.query_params.get('id')
        if id is not None:
            data = Tag.objects.filter(id=id)
        else:
            data = Tag.objects.all()
        return data
    
class DeliveryViewSet(generics.ListAPIView):
    serializer_class = DeliveryConditionSerializer

    def get_queryset(self, *args, **kwargs):
        id = self.request.query_params.get('id')
        if id is not None:
            data = DeliveryCondition.objects.filter(id=id)
        else:
            data = DeliveryCondition.objects.all()
        return data
    

class CategoryViewSet(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self, *args, **kwargs):
        id = self.request.query_params.get('id')
        if id is not None:
            data = Category.objects.filter(id=id)
        else:
            data = Category.objects.all()
        return data
    
class PaymentViewSet(generics.ListAPIView):
    serializer_class = PaymentMethodSerializer

    def get_queryset(self, *args, **kwargs):
        id = self.request.query_params.get('id')
        if id is not None:
            data = PaymentMethod.objects.filter(id=id)
        else:
            data = PaymentMethod.objects.all()
        return data
    
class NewsViewSet(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self, *args, **kwargs):
        id = self.request.query_params.get('id')
        if id is not None:
            data = News.objects.filter(id=id)
        else:
            data = News.objects.all()
        return data
    
    
class SignUpView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def perform_create(self, serializer):
        user, password = serializer.save()
        
        spec = 'Покупатель'
        msg = (
            f"Вы зарегистрировались как {spec}\n"
            f"Ваш login: {user.email}\n"
            f"Ваш password: {password}"
        )

        send_mail(
            "Регистрация в todotodo",
            msg,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'status': 'success',
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)


class StoreViewSet(generics.ListAPIView):
    serializer_class = StoreSerializer

    def get_queryset(self):
        queryset = Store.objects.annotate(product_count=Count('product')).filter(product_count__gt=0)
        return queryset


class BuyerViewSet(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyerSerializer

    def get_queryset(self, *args, **kwargs):
        return [self.request.user.buyer]
    

class OrderViewSet(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self, *args, **kwargs):
        id = self.request.query_params.get('id')
        if id is not None:
            data = Order.objects.filter(id=id)
        else:
            data = Order.objects.all()
        return data
    

class ProvidersViewSet(generics.ListAPIView):
    serializer_class = ProviderSerializer

    def get_queryset(self, *args, **kwargs):
        id = self.request.query_params.get('id')
        queryset = Provider.objects.filter(
            logo__isnull=False,
            company__gt='',
            site__gt='',
            description__gt=''
        )
        
        if id is not None:
            queryset = queryset.filter(id=id)
        
        return queryset
    

class ProviderViewSet(generics.ListAPIView):
    serializer_class = ProviderOnlySerializer

    def get_queryset(self, *args, **kwargs):
        id = self.request.query_params.get('id')
        queryset = Provider.objects.filter(
            logo__isnull=False,
            company__gt='',
            site__gt='',
            description__gt=''
        )
        
        if id is not None:
            queryset = queryset.filter(id=id)
        
        return queryset
    

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        buyer = request.user.buyer
        item = get_object_or_404(Product, id=id)
        store_id = str(item.store.provider.id)

        if store_id in buyer.cart:
            if str(item.id) in buyer.cart[store_id]["items"]:
                buyer.cart[store_id]["items"][str(item.id)]['count'] += int(request.data['count'])
                buyer.cart[store_id]["items"][str(item.id)]['all_price'] += item.price * int(request.data['count'])
            else:
                buyer.cart[store_id]["items"][str(item.id)] = {
                    'photo': item.image.url,
                    'title': item.name + ", " + item.articul,
                    'description': item.description,
                    'price': item.price,
                    'amount': item.amount,
                    'unit': item.unit,
                    'count': int(request.data["count"]),
                    'all_price': item.price * int(request.data['count'])
                }
        else:
            buyer.cart[store_id] = {
                "address": item.store.address,
                "phone": item.store.phone,
                "site": item.store.provider.site,
                "photo": item.store.provider.logo.url,
                "region": item.store.region.name,
                "company": item.store.provider.company,
                "store_id": item.store.id,
                "delivery_conditions": [
                    {"id": delivery_condition.id, "name": delivery_condition.name}
                    for delivery_condition in item.store.delivery_conditions.all()
                ],
                "items": {
                    str(item.id): {
                        'photo': item.image.url,
                        'title': item.name + ", " + item.articul,
                        'description': item.description,
                        'price': item.price,
                        'amount': item.amount,
                        'unit': item.unit,
                        'count': int(request.data["count"]),
                        'all_price': item.price * int(request.data['count'])
                    }
                }
            }

        buyer.total_price += item.price * int(request.data['count'])
        buyer.save()

        return Response({"success": True})

class CartItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        buyer = request.user.buyer
        item = get_object_or_404(Product, id=id)
        store_id = str(item.store.provider.id)

        buyer.total_price -= buyer.cart[store_id]["items"][str(item.id)]["all_price"]
        del buyer.cart[store_id]["items"][str(item.id)]

        if not buyer.cart[store_id]["items"]:
            del buyer.cart[store_id]

        buyer.save()

        return Response({"success": True})

class CartItemMinusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        buyer = request.user.buyer
        item = get_object_or_404(Product, id=id)
        store_id = str(item.store.provider.id)

        buyer.cart[store_id]["items"][str(item.id)]["all_price"] -= buyer.cart[store_id]["items"][str(item.id)]["price"]
        buyer.cart[store_id]["items"][str(item.id)]["count"] -= 1
        buyer.total_price -= buyer.cart[store_id]["items"][str(item.id)]["price"]

        buyer.save()

        return Response({"success": True})

class CartItemPlusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        buyer = request.user.buyer
        item = get_object_or_404(Product, id=id)
        store_id = str(item.store.provider.id)

        buyer.cart[store_id]["items"][str(item.id)]["all_price"] += buyer.cart[store_id]["items"][str(item.id)]["price"]
        buyer.cart[store_id]["items"][str(item.id)]["count"] += 1
        buyer.total_price += buyer.cart[store_id]["items"][str(item.id)]["price"]

        buyer.save()

        return Response({"success": True})
    

class DrawUpOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        buyer = request.user.buyer
        provider = get_object_or_404(Provider, id=id)
        store = get_object_or_404(Store, id=buyer.cart[str(id)]["store_id"])
        delivery_condition = get_object_or_404(DeliveryCondition, name=request.data["delivery"])
        
        order = Order.objects.create(
            buyer=buyer,
            provider=provider,
            store_id=store.id,
            items=buyer.cart[str(id)]["items"],
            total_price=sum(item["all_price"] for item in buyer.cart[str(id)]["items"].values()),
            delivery=delivery_condition,
            address=request.data["address"] if request.data["delivery"] != "Самовывоз" else store.address,
            time=request.data["time"],
            delivery_date=request.data["delivery_date"],
            comment=request.data["comment"]
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

        return Response({"success": True}, status=status.HTTP_201_CREATED)

class AcceptOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        order = get_object_or_404(Order, id=id)
        if order.provider.id != request.user.provider.id:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

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

        return Response({"success": True})

class TransitOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        order = get_object_or_404(Order, id=id)
        if order.provider.id != request.user.provider.id:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

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

        return Response({"success": True})

class SendCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        order = get_object_or_404(Order, id=id)
        if order.provider.id != request.user.provider.id:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

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

        return Response({"success": True})