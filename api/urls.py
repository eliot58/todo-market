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
    path('ads/', AdsViewSet.as_view()),
    path('store/', StoreViewSet.as_view()),
]