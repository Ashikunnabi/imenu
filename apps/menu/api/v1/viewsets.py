from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response

from apps.base.custom_pagination import LargeResultsSetPagination
from apps.base.custom_viewset import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.base.utils.basic import *

from ...services import MenuService, MenuTypeService, MenuItemService
from .serializers import (
    MenuInputSerializer,
    MenuItemInputSerializer,
    MenuItemOutputSerializer,
    MenuOutputSerializer,
    MenuTypeInputSerializer,
    MenuTypeOutputSerializer,
)

User = get_user_model()


class MenuTypeListCreateAPIView(BaseListCreateAPIView):
    service_class = MenuTypeService
    input_serializer_class = MenuTypeInputSerializer
    output_serializer_class = MenuTypeOutputSerializer
    pagination_class = LargeResultsSetPagination

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
        instance = service.create_menu_type(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MenuTypeRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = MenuTypeService
    input_serializer_class = MenuTypeInputSerializer
    output_serializer_class = MenuTypeOutputSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()

        serializer = self.get_input_serializer(
            instance=instance, data=data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        service = self.service_class()
        instance = service.update_menu_type(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "MenuType deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class MenuListCreateAPIView(BaseListCreateAPIView):
    service_class = MenuService
    input_serializer_class = MenuInputSerializer
    output_serializer_class = MenuOutputSerializer
    pagination_class = LargeResultsSetPagination

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
        instance = service.create_menu(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MenuRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = MenuService
    input_serializer_class = MenuInputSerializer
    output_serializer_class = MenuOutputSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()

        serializer = self.get_input_serializer(
            instance=instance, data=data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        service = self.service_class()
        instance = service.update_menu(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "Menu deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class MenuItemListCreateAPIView(BaseListCreateAPIView):
    service_class = MenuItemService
    input_serializer_class = MenuItemInputSerializer
    output_serializer_class = MenuItemOutputSerializer
    pagination_class = LargeResultsSetPagination

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
        instance = service.create_menu_item(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MenuItemRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = MenuItemService
    input_serializer_class = MenuItemInputSerializer
    output_serializer_class = MenuItemOutputSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()

        serializer = self.get_input_serializer(
            instance=instance, data=data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        service = self.service_class()
        instance = service.update_menu_item(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "MenuItem deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
