from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response

from apps.base.custom_pagination import LargeResultsSetPagination
from apps.base.custom_viewset import (
    BaseCreateAPIView,
    BaseListAPIView,
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)

# from apps.finale_inventory.api.v1.viewsets import Finaleinventory.
from apps.base.utils.basic import *

from ...services import (
    AttributeGroupService,
    AttributeService,
    BrandService,
    DocumentService,
    GroupService,
    ProductAttributeService,
    ProductCodeService,
    ProductDocumentService,
    ProductPriceService,
    ProductService,
    ProductWarehouseService,
    SupplierService,
    TypeService,
    WarehouseService,
    ProductUnitService,
    ProductVatService,
    UnitService,
    VatService,
)
from .serializers import (
    AttributeGroupInputSerializer,
    AttributeGroupOutputSerializer,
    AttributeInputSerializer,
    AttributeOutputSerializer,
    BrandInputSerializer,
    BrandOutputSerializer,
    DocumentInputSerializer,
    DocumentOutputSerializer,
    GroupInputSerializer,
    GroupOutputSerializer,
    ProductAttributeInputSerializer,
    ProductAttributeOutputSerializer,
    ProductCodeInputSerializer,
    ProductCodeOutputSerializer,
    ProductCodeQRCodeGenerateInputSerializer,
    ProductCodeQRCodeGenerateOutputSerializer,
    ProductDocumentInputSerializer,
    ProductDocumentOutputSerializer,
    ProductDocumentUploadInputSerializer,
    ProductInputSerializer,
    ProductOutputSerializer,
    ProductPriceInputSerializer,
    ProductPriceOutputSerializer,
    ProductQRCodeGenerateInputSerializer,
    ProductQRCodeGenerateOutputSerializer,
    ProductSearchOutputSerializer,
    ProductUnitInputSerializer,
    ProductUnitOutputSerializer,
    ProductVatInputSerializer,
    ProductVatOutputSerializer,
    ProductWarehouseInputSerializer,
    ProductWarehouseOutputSerializer,
    SupplierInputSerializer,
    SupplierOutputSerializer,
    TypeInputSerializer,
    TypeOutputSerializer,
    UnitInputSerializer,
    UnitOutputSerializer,
    VatInputSerializer,
    VatOutputSerializer,
    WarehouseInputSerializer,
    WarehouseOutputSerializer,
)

# from apps.inventory.stock_transaction import Transaction


User = get_user_model()


class AttributeListCreateAPIView(BaseListCreateAPIView):
    service_class = AttributeService
    input_serializer_class = AttributeInputSerializer
    output_serializer_class = AttributeOutputSerializer
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
        instance = service.create_attribute(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AttributeRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = AttributeService
    input_serializer_class = AttributeInputSerializer
    output_serializer_class = AttributeOutputSerializer

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
        instance = service.update_attribute(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "Attribute deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class AttributeGroupListCreateAPIView(BaseListCreateAPIView):
    service_class = AttributeGroupService
    input_serializer_class = AttributeGroupInputSerializer
    output_serializer_class = AttributeGroupOutputSerializer
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
        instance = service.create_attribute_group(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AttributeGroupRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = AttributeGroupService
    input_serializer_class = AttributeGroupInputSerializer
    output_serializer_class = AttributeGroupOutputSerializer

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
        instance = service.update_attribute_group(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "AttributeGroup deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class BrandListCreateAPIView(BaseListCreateAPIView):
    service_class = BrandService
    input_serializer_class = BrandInputSerializer
    output_serializer_class = BrandOutputSerializer
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
        instance = service.create_brand(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BrandRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = BrandService
    input_serializer_class = BrandInputSerializer
    output_serializer_class = BrandOutputSerializer

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
        instance = service.update_brand(instance=instance, **serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "Brand deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class DocumentListCreateAPIView(BaseListCreateAPIView):
    service_class = DocumentService
    input_serializer_class = DocumentInputSerializer
    output_serializer_class = DocumentOutputSerializer
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
        instance = service.create_document(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DocumentRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = DocumentService
    input_serializer_class = DocumentInputSerializer
    output_serializer_class = DocumentOutputSerializer

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
        instance = service.update_document(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "Document deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class GroupListCreateAPIView(BaseListCreateAPIView):
    service_class = GroupService
    input_serializer_class = GroupInputSerializer
    output_serializer_class = GroupOutputSerializer
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
        instance = service.create_group(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = GroupService
    input_serializer_class = GroupInputSerializer
    output_serializer_class = GroupOutputSerializer

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
        instance = service.update_group(instance=instance, **serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "Group deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductAttributeListCreateAPIView(BaseListCreateAPIView):
    service_class = ProductAttributeService
    input_serializer_class = ProductAttributeInputSerializer
    output_serializer_class = ProductAttributeOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.service_class()
        search = {
            "product__uuid": kwargs["product_uuid"],
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
        validated_data = serializer.validated_data
        validated_data["product_uuid"] = kwargs["product_uuid"]

        service = self.service_class()
        instance = service.create_product_attribute(**validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductAttributeRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = ProductAttributeService
    input_serializer_class = ProductAttributeInputSerializer
    output_serializer_class = ProductAttributeOutputSerializer

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
        validated_data = serializer.validated_data
        validated_data["product_uuid"] = kwargs["product_uuid"]

        service = self.service_class()
        instance = service.update_product_attribute(instance=instance, **validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "ProductAttribute deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductCodeListCreateAPIView(BaseListCreateAPIView):
    service_class = ProductCodeService
    input_serializer_class = ProductCodeInputSerializer
    output_serializer_class = ProductCodeOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.service_class()
        search = {
            "product__uuid": kwargs["product_uuid"],
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
        validated_data["product_uuid"] = kwargs["product_uuid"]

        service = self.service_class()
        instance = service.create_product_code(**validated_data)
        instance = service.detail_response(instance)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductCodeRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = ProductCodeService
    input_serializer_class = ProductCodeInputSerializer
    output_serializer_class = ProductCodeOutputSerializer

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
        instance = service.update_product_code(
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
            {"detail": "ProductCode deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductDocumentListCreateAPIView(BaseListCreateAPIView):
    service_class = ProductDocumentService
    input_serializer_class = ProductDocumentInputSerializer
    output_serializer_class = ProductDocumentOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.service_class()
        search = {
            "product__uuid": kwargs["product_uuid"],
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
        instance = service.create_product_document(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDocumentRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = ProductDocumentService
    input_serializer_class = ProductDocumentInputSerializer
    output_serializer_class = ProductDocumentOutputSerializer

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
        instance = service.update_product_document(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "ProductDocument deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductPriceListCreateAPIView(BaseListCreateAPIView):
    service_class = ProductPriceService
    input_serializer_class = ProductPriceInputSerializer
    output_serializer_class = ProductPriceOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.service_class()
        search = {
            "product__uuid": kwargs["product_uuid"],
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
        validated_data = serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data["product_uuid"] = kwargs["product_uuid"]

        service = self.service_class()
        instance = service.create_product_price(**validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductPriceRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = ProductPriceService
    input_serializer_class = ProductPriceInputSerializer
    output_serializer_class = ProductPriceOutputSerializer

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
        instance = service.update_product_price(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "ProductPrice deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductWarehouseListCreateAPIView(BaseListCreateAPIView):
    service_class = ProductWarehouseService
    input_serializer_class = ProductWarehouseInputSerializer
    output_serializer_class = ProductWarehouseOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.service_class()
        search = {
            "product__uuid": kwargs["product_uuid"],
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
        instance = service.create_product_warehouse(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductWarehouseRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = ProductWarehouseService
    input_serializer_class = ProductWarehouseInputSerializer
    output_serializer_class = ProductWarehouseOutputSerializer

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
        instance = service.update_product_warehouse(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "ProductWarehouse deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class SupplierListCreateAPIView(BaseListCreateAPIView):
    service_class = SupplierService
    input_serializer_class = SupplierInputSerializer
    output_serializer_class = SupplierOutputSerializer
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
        instance = service.create_supplier(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SupplierRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = SupplierService
    input_serializer_class = SupplierInputSerializer
    output_serializer_class = SupplierOutputSerializer

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
        instance = service.update_supplier(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "Supplier deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class TypeListCreateAPIView(BaseListCreateAPIView):
    service_class = TypeService
    input_serializer_class = TypeInputSerializer
    output_serializer_class = TypeOutputSerializer
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
        instance = service.create_type(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TypeRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = TypeService
    input_serializer_class = TypeInputSerializer
    output_serializer_class = TypeOutputSerializer

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
        instance = service.update_type(instance=instance, **serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "Type deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class WarehouseListCreateAPIView(BaseListCreateAPIView):
    service_class = WarehouseService
    input_serializer_class = WarehouseInputSerializer
    output_serializer_class = WarehouseOutputSerializer
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
        instance = service.create_warehouse(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WarehouseRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = WarehouseService
    input_serializer_class = WarehouseInputSerializer
    output_serializer_class = WarehouseOutputSerializer

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
        instance = service.update_warehouse(
            instance=instance, **serializer.validated_data
        )
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "Warehouse deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductListCreateAPIView(BaseListCreateAPIView):
    service_class = ProductService
    input_serializer_class = ProductInputSerializer
    output_serializer_class = ProductOutputSerializer
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
        instance = service.create_product(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = ProductService
    input_serializer_class = ProductInputSerializer
    output_serializer_class = ProductOutputSerializer

    def retrieve(self, request, *args, **kwargs):
        service = self.service_class()
        instance = self.get_object()
        instance.qr_code_path = service.get_qr_code(product_uuid=instance.uuid)
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
        instance = service.update_product(
            instance=instance, **serializer.validated_data
        )
        instance.qr_code_path = service.get_qr_code(product_uuid=instance.uuid)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductQRCodeCreateAPIView(BaseCreateAPIView):
    service_class = ProductService
    input_serializer_class = ProductQRCodeGenerateInputSerializer
    output_serializer_class = ProductQRCodeGenerateOutputSerializer
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


class ProductCodeQRCodeCreateAPIView(BaseCreateAPIView):
    service_class = ProductCodeService
    input_serializer_class = ProductCodeQRCodeGenerateInputSerializer
    output_serializer_class = ProductCodeQRCodeGenerateOutputSerializer
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


class ProductUnitListCreateAPIView(BaseListCreateAPIView):
    service_class = ProductUnitService
    input_serializer_class = ProductUnitInputSerializer
    output_serializer_class = ProductUnitOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.service_class()
        search = {
            "product__uuid": kwargs["product_uuid"],
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
        validated_data = serializer.validated_data
        validated_data["product_uuid"] = kwargs["product_uuid"]

        service = self.service_class()
        instance = service.create_product_unit(**validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductUnitRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = ProductUnitService
    input_serializer_class = ProductUnitInputSerializer
    output_serializer_class = ProductUnitOutputSerializer

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
        validated_data = serializer.validated_data
        validated_data["product_uuid"] = kwargs["product_uuid"]

        service = self.service_class()
        instance = service.update_product_unit(instance=instance, **validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "ProductUnit deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductVatListCreateAPIView(BaseListCreateAPIView):
    service_class = ProductVatService
    input_serializer_class = ProductVatInputSerializer
    output_serializer_class = ProductVatOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.service_class()
        search = {
            "product__uuid": kwargs["product_uuid"],
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
        validated_data = serializer.validated_data
        validated_data["product_uuid"] = kwargs["product_uuid"]

        service = self.service_class()
        instance = service.create_product_vat(**validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductVatRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = ProductVatService
    input_serializer_class = ProductVatInputSerializer
    output_serializer_class = ProductVatOutputSerializer

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
        validated_data = serializer.validated_data
        validated_data["product_uuid"] = kwargs["product_uuid"]

        service = self.service_class()
        instance = service.update_product_vat(instance=instance, **validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "ProductVat deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class UnitListCreateAPIView(BaseListCreateAPIView):
    service_class = UnitService
    input_serializer_class = UnitInputSerializer
    output_serializer_class = UnitOutputSerializer
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
        instance = service.create_unit(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnitRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = UnitService
    input_serializer_class = UnitInputSerializer
    output_serializer_class = UnitOutputSerializer

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
        instance = service.update_unit(instance=instance, **serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "Unit deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class VatListCreateAPIView(BaseListCreateAPIView):
    service_class = VatService
    input_serializer_class = VatInputSerializer
    output_serializer_class = VatOutputSerializer
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
        instance = service.create_vat(**serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VatRetrieveUpdateDestroyAPIView(BaseRetrieveUpdateDestroyAPIView):
    service_class = VatService
    input_serializer_class = VatInputSerializer
    output_serializer_class = VatOutputSerializer

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
        instance = service.update_vat(instance=instance, **serializer.validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        service = self.service_class()
        service.delete(instance=instance)
        return Response(
            {"detail": "Vat deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductDocumentUploadAPIView(BaseCreateAPIView):
    service_class = ProductService
    input_serializer_class = ProductDocumentUploadInputSerializer
    output_serializer_class = ProductDocumentOutputSerializer
    pagination_class = LargeResultsSetPagination

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_input_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data["product_uuid"] = kwargs["product_uuid"]

        service = self.service_class()
        instance = service.upload_document(**validated_data)
        serializer = self.get_output_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductSearchAPIView(BaseListAPIView):
    service_class = ProductService
    input_serializer_class = ProductInputSerializer
    output_serializer_class = ProductSearchOutputSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        service = self.service_class()
        search = {
            "search": request.GET.get("search[value]", request.GET.get("q", None))
        }
        queryset = service.list(**search)

        page = self.paginate_queryset(queryset)
        if page is not None:
            data = service.product_search_list_response(page)
            serializer = self.get_output_serializer(data, many=True)
            return self.get_paginated_response(serializer.data)

        data = service.product_search_list_response(queryset)
        serializer = self.get_output_serializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
