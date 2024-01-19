from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response

from apps.base.custom_pagination import LargeResultsSetPagination
from apps.base.custom_viewset import BaseListCreateAPIView, BaseRetrieveUpdateAPIView
from apps.base.utils.basic import *
from apps.order.services.order_service import OrderService

from .serializers import DashboardOrderInputSerializer, DashboardOrderOutputSerializer

User = get_user_model()


class OrderListCreateAPIView(BaseListCreateAPIView):
    service_class = OrderService
    input_serializer_class = DashboardOrderInputSerializer
    output_serializer_class = DashboardOrderOutputSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        service = self.service_class()
        search = {
            "search": request.GET.get("search[value]", request.GET.get("q", None))
        }
        queryset = service.list(**search)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_output_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_output_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_input_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        service = self.service_class()
        instance = service.create_order(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderRetrieveUpdateAPIView(BaseRetrieveUpdateAPIView):
    service_class = OrderService
    input_serializer_class = DashboardOrderInputSerializer
    output_serializer_class = DashboardOrderOutputSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_input_serializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        service = self.service_class()
        instance = self.get_object()
        instance = service.update_model_instance(instance=instance, **serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
