from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .viewsets import *


app_name = 'v1'


router = DefaultRouter()
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
