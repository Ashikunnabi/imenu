from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response

from apps.base.custom_pagination import LargeResultsSetPagination
from apps.base.custom_viewset import (
    BaseCreateAPIView,
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.base.utils.basic import *

from ...services import (
    TableService,
    TableTypeService,
    TableCodeService,
    TableDocumentService,
)
from .serializers import (
    TableCodeInputSerializer,
    TableCodeOutputSerializer,
    TableCodeQRCodeGenerateInputSerializer,
    TableCodeQRCodeGenerateOutputSerializer,
    TableDocumentInputSerializer,
    TableDocumentOutputSerializer,
    TableDocumentUploadInputSerializer,
    TableInputSerializer,
    TableOutputSerializer,
    TableTypeInputSerializer,
    TableTypeOutputSerializer,
)

User = get_user_model()


class TableTypeListCreateAPIView(BaseListCreateAPIView):
    service_class = TableTypeService
    input_serializer_class = TableTypeInputSerializer
    output_serializer_class = TableTypeOutputSerializer
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
        instance = service.create_table_type(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TableTypeRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = TableTypeService
    input_serializer_class = TableTypeInputSerializer
    output_serializer_class = TableTypeOutputSerializer

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
        instance = service.update_table_type(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "TableType deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class TableListCreateAPIView(BaseListCreateAPIView):
    service_class = TableService
    input_serializer_class = TableInputSerializer
    output_serializer_class = TableOutputSerializer
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
        instance = service.create_table(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TableRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = TableService
    input_serializer_class = TableInputSerializer
    output_serializer_class = TableOutputSerializer

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
        instance = service.update_table(instance=instance, **serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "Table deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class TableCodeListCreateAPIView(BaseListCreateAPIView):
    service_class = TableCodeService
    input_serializer_class = TableCodeInputSerializer
    output_serializer_class = TableCodeOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.service_class()
        search = {
            "table__uuid": kwargs["table_uuid"],
            "search": request.GET.get("search[value]", None),
        }
        queryset = service.list(**search)

        page = self.paginate_queryset(queryset)
        if page is not None:
            page = service.list_response(page)
            serializer = self.get_output_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_output_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_input_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data["table_uuid"] = kwargs["table_uuid"]

        service = self.service_class()
        instance = service.create_table_code(**validated_data)
        instance = service.detail_response(instance)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TableCodeRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = TableCodeService
    input_serializer_class = TableCodeInputSerializer
    output_serializer_class = TableCodeOutputSerializer

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
        instance = service.update_table_code(
            instance=instance, **serializer.validated_data
        )
        instance = service.detail_response(instance)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "TableCode deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class TableCodeQRCodeCreateAPIView(BaseCreateAPIView):
    service_class = TableCodeService
    input_serializer_class = TableCodeQRCodeGenerateInputSerializer
    output_serializer_class = TableCodeQRCodeGenerateOutputSerializer
    pagination_class = LargeResultsSetPagination

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_input_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["uuid"] = self.kwargs["uuid"]

        service = self.service_class()
        path = service.generate_qr_code(**data)
        serializer = self.get_output_serializer(instance={"path": path})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TableDocumentListCreateAPIView(BaseListCreateAPIView):
    service_class = TableDocumentService
    input_serializer_class = TableDocumentInputSerializer
    output_serializer_class = TableDocumentOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.service_class()
        search = {
            "table__uuid": kwargs["table_uuid"],
            "search": request.GET.get("search[value]", None),
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
        instance = service.create_table_document(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TableDocumentRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = TableDocumentService
    input_serializer_class = TableDocumentInputSerializer
    output_serializer_class = TableDocumentOutputSerializer

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
        instance = service.update_table_document(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "TableDocument deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class TableDocumentUploadAPIView(BaseCreateAPIView):
    service_class = TableService
    input_serializer_class = TableDocumentUploadInputSerializer
    output_serializer_class = TableDocumentOutputSerializer
    pagination_class = LargeResultsSetPagination

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_input_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data["table_uuid"] = kwargs["table_uuid"]

        service = self.service_class()
        instance = service.upload_document(**validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)