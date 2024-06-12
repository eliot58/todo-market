from rest_framework import generics
from core.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

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
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


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
    

class ProviderViewSet(generics.ListAPIView):
    serializer_class = ProviderSerializer

    def get_queryset(self, *args, **kwargs):
        id = self.request.query_params.get('id')
        if id is not None:
            data = Provider.objects.filter(id=id)
        else:
            data = Provider.objects.all()
        return data