from django.urls import include, path
from .views import *


app_name = "front_end"

urlpatterns = [
    path("", index, name="index"),
    path("product-detail/<uuid:uuid>/", product_detail, name="product_detail"),
    path("favorite/", favorite, name="favorite"),
    path("cart/", cart, name="cart"),
    path("account/", account, name="account"),
    path("change_password/", change_password, name="change_password"),
    path("chat/", chat, name="chat"),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path("category/", category, name="category"),
    path("category/<uuid:uuid>/product-list/", product_list, name="product_list"),
]
