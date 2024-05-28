from django.urls import path
from .handlers.common import index, partner, delivery, news, providers, provider
from .handlers.auth import login_view, logout_view, signup
from .handlers.profile import provider_profile, buyer_profile, upload_files
from .handlers.store import create_store, update_store, delete_store, storeProducts
from .handlers.product import create_product, update_product, delete_product
from .handlers.cart import cart, cart_item_delete, cart_item_minus, cart_item_plus, addtoCart
from .handlers.order import orders, order, drawup, accept, send_check, transit
from .handlers.subscriptions import susbscriptions, payment_webhook

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
    path("provider_profile/", provider_profile, name="provider_profile"),
    path("create_store/", create_store, name="create_store"),
    path("delete_store/<int:id>/", delete_store, name="delete_store"),
    path("update_store/<int:id>/", update_store, name="update_store"),
    path("create_product/", create_product, name="create_product"),
    path("update_product/<int:id>/", update_product, name="update_product"),
    path("delete_product/<int:id>/", delete_product, name="delete_product"),
    path("upload_files/", upload_files, name="upload_files"),
    path('cart/', cart, name='cart'),
    path('addtoCart/<int:id>/', addtoCart, name='addtoCart'),
    path('cart_item_delete/<str:id>/', cart_item_delete, name="cart_item_delete"),
    path('minus/<int:id>/', cart_item_minus),
    path('plus/<int:id>/', cart_item_plus),
    path("storeProducts/<int:id>/", storeProducts, name="store_products"),
    path("susbscriptions/", susbscriptions, name="susbscriptions"),
    path("drawup/<int:id>/", drawup, name="drawup"),
    path("orders/", orders, name="orders"),
    path("order/<int:id>/", order, name="order"),
    path("buyer_profile/", buyer_profile, name="buyer_profile"),
    path("accept/<int:id>/", accept, name="accept"),
    path("send_check/<int:id>/", send_check, name="send_check"),
    path("transit/<int:id>/", transit, name="transit"),
    path('webhook/', payment_webhook, name='payment_webhook'),
]