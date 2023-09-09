from django.urls import path

from .viewsets import (
    CartLineListCreateAPIView,
    CartLineRetrieveUpdateDestroyAPIView,
    CartListCreateAPIView,
)

app_name = "v1"

urlpatterns = [
    path(
        "carts/",
        CartListCreateAPIView.as_view(),
        name="cart-list-create",
    ),
    path(
        "carts/<uuid:cart_uuid>/",
        CartLineListCreateAPIView.as_view(),
        name="cart-line-list-create",
    ),
    path(
        "carts/<uuid:cart_uuid>/lines/<uuid:uuid>/",
        CartLineRetrieveUpdateDestroyAPIView.as_view(),
        name="cart-line-list-create",
    ),
]
