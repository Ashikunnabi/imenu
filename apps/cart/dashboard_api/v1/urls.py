from django.urls import path

from .viewsets import (
    CartLineListCreateAPIView,
    CartLineRetrieveUpdateDestroyAPIView,
    CartListCreateAPIView,
    CartRetrieveAPIView,
)

app_name = "v1"

urlpatterns = [
    path(
        "",
        CartListCreateAPIView.as_view(),
        name="dashboard_cart_list_create",
    ),
    path(
        "<uuid:uuid>/",
        CartRetrieveAPIView.as_view(),
        name="dashboard_cart_retrieve",
    ),
    path(
        "<uuid:cart_uuid>/lines/",
        CartLineListCreateAPIView.as_view(),
        name="dashboard_cart_line_list_create",
    ),
    path(
        "<uuid:cart_uuid>/lines/<uuid:uuid>/",
        CartLineRetrieveUpdateDestroyAPIView.as_view(),
        name="dashboard_cart_line_retrieve_update_destroy",
    ),
]
