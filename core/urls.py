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
    path("providers/", providers, name="providers"),
    path("provider/<int:id>/", provider, name="provider"),
    path("profile/", profile, name="profile"),
    path("create_store/", create_store, name="create_store"),
    path("delete_store/<int:id>/", delete_store, name="delete_store"),
    path("update_store/<int:id>/", update_store, name="update_store"),
    path("create_product/", create_product, name="create_product"),
    path("update_product/<int:id>/", update_product, name="update_product"),
    path("delete_product/<int:id>/", delete_product, name="delete_product"),
    path("upload_files/", upload_files, name="upload_files"),
]