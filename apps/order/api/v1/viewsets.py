from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.base.custom_pagination import LargeResultsSetPagination
from apps.base.utils.basic import *

from ...models.order import Order
from .serializers import OrderSerializer

User = get_user_model()


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "uuid"  # Individual object will be found by this field
