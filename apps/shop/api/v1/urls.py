from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .viewsets import *


app_name = "v1"


router = DefaultRouter()
router.Register(r"shop", ShopViewSet, basename="shop")
router.Register(r"shopkeeper", ShopkeeperViewSet, basename="shopkeeper")
router.Register(r"shop-product", ShopProductViewSet, basename="shop-product")
router.Register(r"shop-order", ShopOrderViewSet, basename="shop-order")
router.Register(r"shop-order-pos", ShopOrderPOSViewSet, basename="shop-order-pos")

urlpatterns = [
    path("", include(router.urls)),
]
