from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', SignUpView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('region/', RegionViewSet.as_view()),
    path('tag/', RegionViewSet.as_view()),
    path('delivery/', DeliveryViewSet.as_view()),
    path('category/', CategoryViewSet.as_view()),
    path('payment/', PaymentViewSet.as_view()),
    path('news/', NewsViewSet.as_view()),
    path('store/', StoreViewSet.as_view()),
    path('buyer/', BuyerViewSet.as_view()),
    path('order/', OrderViewSet.as_view()),
    path('providers/', ProvidersViewSet.as_view()),
    path('provider/', ProviderViewSet.as_view()),
    path('add_to_cart/<int:id>/', AddToCartView.as_view()),
    path('cart_item_delete/<int:id>/', CartItemDeleteView.as_view()),
    path('cart_item_minus/<int:id>/', CartItemMinusView.as_view()),
    path('cart_item_plus/<int:id>/', CartItemPlusView.as_view()),
    path('draw_up/<int:id>/', DrawUpOrderView.as_view()),
    path('accept/<int:id>/', AcceptOrderView.as_view()),
    path('transit/<int:id>/', TransitOrderView.as_view()),
    path('send_check/<int:id>/', SendCheckView.as_view()),
]