from rest_framework import serializers
from core.models import *


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class DeliveryConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCondition
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=256)
    fullName = serializers.CharField(max_length=256)

    def validate_email(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_phone(self, value):
        if Buyer.objects.filter(phone=value).exists() or Provider.objects.filter(phone=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        return value

    def create(self, validated_data):
        password = User.objects.make_random_password(length=8)
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email']
        )
        user.set_password(password)
        user.save()

        Buyer.objects.create(
            user=user,
            phone=validated_data['phone'],
            fullName=validated_data['fullName']
        )

        return user, password

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True, source='product_set')

    class Meta:
        model = Store
        fields = '__all__'