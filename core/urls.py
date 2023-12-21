from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("login/", login_view, name="login_view"),
    path('logout/', logout_view, name='logout_core_view'),
    path("register/", signup, name="signup"),
    path("partner/", partner, name="partner"),
    path("delivery/", delivery, name="delivery"),
    path("news/", news, name="news"),
    path("providers/", providers, name="providers")
]