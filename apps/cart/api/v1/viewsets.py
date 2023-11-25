from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions

from apps.base.custom_pagination import LargeResultsSetPagination
from apps.base.custom_viewset import (
    BaseListCreateAPIView,
    BaseRetrieveAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)

from apps.base.utils.basic import *

from ...services import CartService, CartLineService
from .serializers import (
    CartInputSerializer,
    CartLineInputSerializer,
    CartLineOutputSerializer,
    CartOutputSerializer,
)


class CartListCreateAPIView(BaseListCreateAPIView):
    service_class = CartService
    input_serializer_class = CartInputSerializer
    output_serializer_class = CartOutputSerializer
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
        instance = service.create_cart(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartRetrieveAPIView(BaseRetrieveAPIView):
    service_class = CartService
    input_serializer_class = CartInputSerializer
    output_serializer_class = CartOutputSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartLineListCreateAPIView(BaseListCreateAPIView):
    service_class = CartLineService
    cart_service_class = CartService
    input_serializer_class = CartLineInputSerializer
    output_serializer_class = CartOutputSerializer
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
        validated_data = serializer.validated_data
        validated_data["cart_uuid"] = kwargs["cart_uuid"]

        service = self.service_class()
        cart_service = self.cart_service_class()
        instance = service.create_cart_line(**validated_data)
        cart_service.calculate_price(cart=instance.cart)
        serializer = self.get_output_serializer(instance.cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartLineRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = CartLineService
    cart_service_class = CartService
    input_serializer_class = CartLineInputSerializer
    output_serializer_class = CartOutputSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()

        serializer = self.get_input_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        service = self.service_class()
        cart_service = self.cart_service_class()
        instance = service.update_cart_line(
            instance=instance, **serializer.validated_data
        )
        cart_service.calculate_price(cart=instance.cart)
        serializer = self.get_output_serializer(instance.cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        cart_service = self.cart_service_class()
        cart_service.calculate_price(cart=instance.cart)
        serializer = self.get_output_serializer(instance.cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
