from django.urls import path

from .viewsets import *

app_name = "v1"


urlpatterns = [
    path(
        "",
        OrderListCreateAPIView.as_view(),
        name="order_list_create",
    ),
    path(
        "<uuid:uuid>/",
        OrderRetrieveAPIView.as_view(),
        name="order_retrieve",
    ),
]
