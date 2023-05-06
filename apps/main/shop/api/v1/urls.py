from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .viewsets import *


app_name = "v1"


router = DefaultRouter()
router.register(r"shop", ShopViewSet, basename="shop")
router.register(r"shopkeeper", ShopkeeperViewSet, basename="shopkeeper")
router.register(r"shop-product", ShopProductViewSet, basename="shop-product")
router.register(r"shop-order", ShopOrderViewSet, basename="shop-order")
router.register(r"shop-order-pos", ShopOrderPOSViewSet, basename="shop-order-pos")

urlpatterns = [
    path("", include(router.urls)),
]
