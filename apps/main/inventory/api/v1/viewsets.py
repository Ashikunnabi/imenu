from django.contrib.auth import get_user_model
from apps.main.inventory.services.product_unit_service import ProductUnitService
from apps.main.inventory.services.product_vat_service import ProductVatService
from apps.main.inventory.services.unit_service import UnitService
from apps.main.inventory.services.vat_service import VatService
from rest_framework import status
from rest_framework.response import Response

from apps.core.base.custom_pagination import (
    LargeResultsSetPagination,
)
from apps.core.base.custom_viewset import (
    BaseCreateAPIView,
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)

# from apps.main.finale_inventory.api.v1.viewsets import FinaleInventory
from apps.core.base.utils.basic import *

# from apps.main.inventory.stock_transaction import Transaction

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
    ProductInputSerializer,
    ProductOutputSerializer,
    ProductPriceInputSerializer,
    ProductPriceOutputSerializer,
    ProductQRCodeGenerateInputSerializer,
    ProductQRCodeGenerateOutputSerializer,
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

    # @action(detail=False, methods=["POST"], name="Delete Multiple Product")
    # def delete_multiple_product(self, request, *args, **kwargs):
    #     products = request.data.get("product_uuid", [])
    #     for product_uuid in products:
    #         instance = Product.objects.get(uuid=product_uuid)
    #         self.perform_soft_delete(instance, request)
    #     return Response(
    #         {"detail": "Product deleted successfully"}, status=status.HTTP_200_OK
    #     )

    # @action(detail=False, methods=["GET"], name="Sync Product")
    # def sync_from_finale(self, request, *args, **kwargs):
    #     # authenticate to finale inventory
    #     try:
    #         finale_inventory = FinaleInventory(
    #             settings.FINALE_URL,
    #             settings.FINALE_USERNAME,
    #             settings.FINALE_PASSWORD,
    #         )

    #         # request for manufacturer
    #         response = finale_inventory.get_product_list(
    #             {
    #                 "operationName": None,
    #                 "variables": {},
    #                 "query": "query Rows($after: String, $first: Int) { "
    #                 'productViewConnection(status: ["PRODUCT_ACTIVE"], '
    #                 'after: $after, first: $first, sort: [{field: "productId", '
    #                 'mode: "asc"}]) { edges { node(timezone: "Asia/Dhaka")'
    #                 " { "
    #                 "amazonStandardIdentificationNumber "
    #                 "averageCost "
    #                 "caliber "
    #                 "category "
    #                 "description"
    #                 " imageTooltip { description }"
    #                 "itemPrice "
    #                 "manufacturer "
    #                 "mfgProductId "
    #                 "neqPerUnit "
    #                 'productId(formatter: "html") '
    #                 "status "
    #                 "unitOfMeasure "
    #                 "unitsInStock "
    #                 "universalProductCode "
    #                 "valuation "
    #                 "}}}}",
    #             }
    #         )

    #         if response["status"]:
    #             # successful response
    #             product_list = response["data"]
    #             product_objects, product_objects_update = [], []

    #             for product in product_list:
    #                 product = product["node"]
    #                 # product_id = ((product['productId']).split('href="?product/detail/')[1]).split('">')[0]
    #                 product_id = ((product["productId"]).split('">')[1]).split("</a>")[
    #                     0
    #                 ]
    #                 try:
    #                     part_no = product_id.split(" ")[1]
    #                 except Exception:
    #                     part_no = product_id
    #                 category = (
    #                     None
    #                     if product["category"] in ["", None]
    #                     else ProductCategory.objects.get(name=product["category"])
    #                 )

    #                 all_brand_names_alphanum = {}
    #                 for val in Brand.objects.values("name", "id"):
    #                     all_brand_names_alphanum[
    #                         re.sub(r"[^A-Za-z0-9]", "", val.name).lower()
    #                     ] = val.id

    #                 manufacturer_name_alphanum = re.sub(
    #                     r"[^A-Za-z0-9]", "", product["manufacturer"].strip()
    #                 ).lower()
    #                 try:
    #                     manufacturer = (
    #                         None
    #                         if product["manufacturer"] in ["", None]
    #                         else Brand.objects.get(
    #                             id=all_brand_names_alphanum[
    #                                 manufacturer_name_alphanum
    #                             ].id
    #                         )
    #                     )
    #                 except Exception as ex:
    #                     continue

    #                 if not Product.objects.filter(product_id=product_id).exists():
    #                     try:
    #                         addable_product = Product(
    #                             uuid=random_hex_code(length=16),
    #                             product_id=product_id,
    #                             description=product["description"],
    #                             part_no=part_no,
    #                             # single_price=product['productId'],
    #                             # your_price=product['productId'],
    #                             # retail_price=product['productId'],
    #                             # map_price=product['productId'],
    #                             # jobbar_price=product['productId'],
    #                             finale_detail_url=f"?product/details/{product_id}",
    #                             amazon_standard_identification_number=product[
    #                                 "amazonStandardIdentificationNumber"
    #                             ],
    #                             average_cost=product["averageCost"],
    #                             caliber=product["caliber"],
    #                             category=category,
    #                             item_price=product["itemPrice"],
    #                             manufacturer=manufacturer,
    #                             mfg_product_id=product["mfgProductId"],
    #                             neq_per_unit=product["neqPerUnit"],
    #                             unit_of_measure=product["unitOfMeasure"],
    #                             universal_product_code=product["universalProductCode"],
    #                             valuation=product["valuation"],
    #                             image_url=product["imageTooltip"]["description"],
    #                             image=None,
    #                             created_by=request.instance.id,
    #                             updated_by=request.instance.id,
    #                         )
    #                     except Exception as ex:
    #                         addable_product = None
    #                         logging.getLogger("warning_logger").warning(ex.__str__())
    #                     if addable_product:
    #                         product_objects.append(addable_product)
    #                 else:
    #                     is_product_updatable = Product.objects.filter(
    #                         product_id=product_id,
    #                         sync_from_finale=True,
    #                         is_soft_deleted=False,
    #                     )
    #                     if is_product_updatable.exist():
    #                         product_update = is_product_updatable.first()
    #                         product_update.description = product["description"]
    #                         product_update.part_no = part_no
    #                         # product_update.single_price = product['productId']
    #                         # product_update.your_price = product['productId']
    #                         # product_update.retail_price = product['productId']
    #                         # product_update.map_price = product['productId']
    #                         # product_update.jobbar_price = product['productId']
    #                         product_update.amazon_standard_identification_number = (
    #                             product["amazonStandardIdentificationNumber"]
    #                         )
    #                         product_update.average_cost = product["averageCost"]
    #                         product_update.caliber = product["caliber"]
    #                         product_update.category = category
    #                         product_update.item_price = product["itemPrice"]
    #                         product_update.manufacturer = manufacturer
    #                         product_update.mfg_product_id = product["mfgProductId"]
    #                         product_update.neq_per_unit = product["neqPerUnit"]
    #                         product_update.unit_of_measure = product["unitOfMeasure"]
    #                         product_update.universal_product_code = product[
    #                             "universalProductCode"
    #                         ]
    #                         product_update.valuation = product["valuation"]
    #                         product_update.image_url = product["imageTooltip"][
    #                             "description"
    #                         ]
    #                         product_update.updated_by = request.instance.id
    #                         product_update.is_active = (
    #                             True if product["status"] == "Active" else False
    #                         )

    #                         product_model_fields = [
    #                             field.name for field in Product._meta.get_fields()
    #                         ]
    #                         current_product_object = Product.objects.get(
    #                             product_id=product_id
    #                         )
    #                         for field in product_model_fields:
    #                             if getattr(
    #                                 current_product_object,
    #                                 current_product_object._meta.get_field(
    #                                     field
    #                                 ).attname,
    #                             ) != getattr(
    #                                 product_update,
    #                                 product_update._meta.get_field(field).attname,
    #                             ):
    #                                 product_update.save()
    #                                 product_objects_update.append(product_update.id)
    #                                 break

    #             if len(product_objects):
    #                 products = Product.objects.bulk_create(product_objects)

    #             if len(product_objects_update):
    #                 update_products = Product.objects.filter(
    #                     id__in=product_objects_update
    #                 )
    #             return Response(
    #                 {"details": "Product synced successfully"},
    #                 status=status.HTTP_200_OK,
    #             )
    #         else:
    #             return Response(
    #                 {"details": "Product synced failed"},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )
    #     except Exception as ex:
    #         return Response(
    #             {"details": ex.__str__()}, status=status.HTTP_400_BAD_REQUEST
    #         )

    # @action(detail=False, methods=["GET"], name="Get Live Stock")
    # def get_live_stock(self, request, *args, **kwargs):
    #     product_id = self.request.query_params.get("product_id")

    #     if product_id is None:
    #         return Response(
    #             {"details": "Product ID required"}, status=status.HTTP_400_BAD_REQUEST
    #         )

    #     try:
    #         # authenticate to finale
    #         finale_inventory = FinaleInventory(
    #             settings.FINALE_URL,
    #             settings.FINALE_USERNAME,
    #             settings.FINALE_PASSWORD,
    #         )
    #         # request for product
    #         response = finale_inventory.get_product_details(
    #             {
    #                 "operationName": None,
    #                 "variables": {},
    #                 "query": "query Rows($after: String, $first: Int) { "
    #                 'productViewConnection(status: ["PRODUCT_ACTIVE"], '
    #                 f'search: "{product_id}", '
    #                 'after: $after, first: $first, sort: [{field: "productId", '
    #                 'mode: "asc"}]) { edges { node(timezone: "Asia/Dhaka")'
    #                 " { "
    #                 "unitsInStock "
    #                 "}}}}",
    #             }
    #         )

    #         if response["status"]:
    #             # successful response
    #             available_stock = response["data"][0]["node"]["unitsInStock"]
    #             return Response(
    #                 {"data": {"available_stock": available_stock}},
    #                 status=status.HTTP_200_OK,
    #             )
    #         else:
    #             return Response(
    #                 {"details": "Product synced failed"},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )
    #     except Exception as ex:
    #         return Response(
    #             {"details": ex.__str__()}, status=status.HTTP_400_BAD_REQUEST
    #         )

    # @action(detail=False, methods=["POST"], name="Upload product price sheet")
    # def upload_price_sheet(self, request, *args, **kwargs):
    #     product_price_sheet = self.request.FILES.get("file")

    #     if product_price_sheet is None:
    #         return Response(
    #             {"details": "No file found"}, status=status.HTTP_400_BAD_REQUEST
    #         )

    #     if not product_price_sheet.name.endswith(".csv"):
    #         return Response(
    #             {"details": "Only csv file allowed"}, status=status.HTTP_400_BAD_REQUEST
    #         )

    #     # store files in server
    #     file_path = f"{settings.PRODUCT_PRICE_SHEET}{product_price_sheet.name}"
    #     path = default_storage.save(file_path, product_price_sheet)

    #     # check file code utf-8 or not
    #     try:
    #         codecs.open(
    #             default_storage.path(path), mode="r", encoding="utf-8", errors="strict"
    #         ).readlines()
    #     except UnicodeDecodeError:
    #         default_storage.delete(path)
    #         return Response(
    #             {"details": "Invalid File Format (UTF-8 required)"},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    #     # read csv file and update product price
    #     with open(
    #         default_storage.path(path), mode="r", encoding="utf-8-sig"
    #     ) as csv_file:
    #         csv_reader = csv.DictReader(csv_file)
    #         try:
    #             for row in csv_reader:
    #                 product = Product.objects.filter(product_id=row["PRODUCT_ID"])
    #                 if product.exists():
    #                     product = product[0]
    #                     product.single_price = row["SINGLE_PRICE"]
    #                     product.your_price = row["YOUR_COST"]
    #                     product.retail_price = row["RETAIL_PRICE"]
    #                     product.map_price = row["MAP_PRICE"]
    #                     product.jobbar_price = row["JOBBER_PRICE"]
    #                     product.universal_product_code = row.get(
    #                         "UPC", product.universal_product_code
    #                     )
    #                     if row.get("IMAGE_URL"):
    #                         product.image = None
    #                         product.image_url = row.get("IMAGE_URL", None)

    #                     if row.get("CATEGORY"):
    #                         product.category = ProductCategory.objects.get(
    #                             uuid=row.get("CATEGORY")
    #                         )
    #                     if row.get("BRAND"):
    #                         product.manufacturer = Brand.objects.get(
    #                             uuid=row.get("BRAND")
    #                         )
    #                     product.stock = row.get("STOCK", product.stock)

    #                     # warehouse data update
    #                     available_columns = csv_reader.fieldnames
    #                     warehouses = warehouse.objects.filter(is_active=True)

    #                     for warehouse in warehouses:
    #                         if not ProductInwarehouse.objects.filter(
    #                             product=product, warehouse=warehouse
    #                         ).exists():
    #                             product_in_warehouse = (
    #                                 ProductInwarehouse.objects.create(
    #                                     product=product, warehouse=warehouse
    #                                 )
    #                             )
    #                         else:
    #                             product_in_warehouse = ProductInwarehouse.objects.get(
    #                                 product=product, warehouse=warehouse
    #                             )

    #                         if f"WAREHOUSE {warehouse.name}" in available_columns:
    #                             if row.get(f"WAREHOUSE {warehouse.name}", "0") not in [
    #                                 "0",
    #                                 "",
    #                                 None,
    #                             ]:
    #                                 product_in_warehouse.stock = row.get(
    #                                     f"WAREHOUSE {warehouse.name}", "0"
    #                                 )
    #                                 product_in_warehouse.save()

    #                     product.save()
    #                 else:
    #                     product = Product()
    #                     product.product_id = row["PRODUCT_ID"]
    #                     product.description = row["DESCRIPTION"]
    #                     product.part_no = row["PART_NUMBER"]
    #                     product.single_price = row["SINGLE_PRICE"]
    #                     product.your_price = row["YOUR_COST"]
    #                     product.retail_price = row["RETAIL_PRICE"]
    #                     product.map_price = row["MAP_PRICE"]
    #                     product.jobbar_price = row["JOBBER_PRICE"]
    #                     product.image_url = row.get("IMAGE_URL", None)
    #                     product.category = ProductCategory.objects.get(
    #                         uuid=row.get("CATEGORY")
    #                     )
    #                     product.manufacturer = Brand.objects.get(
    #                         uuid=row.get("BRAND")
    #                     )
    #                     product.universal_product_code = row["UPC"]
    #                     product.stock = row["STOCK"] if row.get("STOCK") else None
    #                     product.sync_from_finale = False
    #                     product.added_from_finale = False
    #                     product.save()

    #                     # warehouse data update
    #                     available_columns = csv_reader.fieldnames
    #                     warehouses = warehouse.objects.filter(is_active=True)

    #                     for warehouse in warehouses:
    #                         if not ProductInwarehouse.objects.filter(
    #                             product=product, warehouse=warehouse
    #                         ).exists():
    #                             product_in_warehouse = (
    #                                 ProductInwarehouse.objects.create(
    #                                     product=product, warehouse=warehouse
    #                                 )
    #                             )
    #                         else:
    #                             product_in_warehouse = ProductInwarehouse.objects.get(
    #                                 product=product, warehouse=warehouse
    #                             )

    #                         if f"WAREHOUSE {warehouse.name}" in available_columns:
    #                             product_in_warehouse.stock = row.get(
    #                                 f"WAREHOUSE {warehouse.name}", "0"
    #                             )
    #                             product_in_warehouse.save()
    #         except ProductCategory.DoesNotExist:
    #             return Response(
    #                 {"details": f"{row['PART_NUMBER']}: Category does not exists."},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )
    #         except Brand.DoesNotExist:
    #             return Response(
    #                 {"details": f"{row['PART_NUMBER']}: Brand does not exists."},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )
    #         except Exception as ex:
    #             return Response(
    #                 {"details": f"{row['PART_NUMBER']}: {ex.__str__()}"},
    #                 status=status.HTTP_400_BAD_REQUEST,
    #             )

    #     return Response({"details": "Product price updated"}, status=status.HTTP_200_OK)

    # @action(detail=False, methods=["GET"], name="Search product")
    # def search(self, request, *args, **kwargs):
    #     query_param = self.request.GET.get("q")

    #     if query_param == "":
    #         return Response({"data": []}, status=status.HTTP_200_OK)

    #     # inactive brand for dealer
    #     inactive_brands_id = DealerBrand.objects.filter(
    #         dealer=request.instance, is_active=False
    #     ).values_list("brand_id", flat=True)

    #     queryset = self.get_queryset().filter(
    #         Q(manufacturer__name__icontains=query_param)
    #         | Q(description__icontains=query_param)
    #         | Q(part_no__icontains=query_param),
    #         is_active=True,
    #         category__is_active=True,
    #         is_soft_deleted=False,
    #     )

    #     # remove inactive brands product for dealer
    #     if not request.instance.is_staff:
    #         queryset = queryset.exclude(
    #             Q(manufacturer__is_active=False)
    #             | Q(manufacturer_id__in=inactive_brands_id)
    #         )[:10]

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response({"data": serializer.data}, status=status.HTTP_200_OK)


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


# def is_authorized_dealer(brand: Brand, dealer: User) -> bool:
#     """Check a dealer is authorized for buying a product from a brand."""
#     if not brand.is_authorization_required:
#         return True

#     is_authorized = DealerBrand.objects.filter(
#         brand=brand, dealer=dealer, is_authorized=True
#     ).exists()
#     return is_authorized


# def get_products_with_custom_column(products, instance: User) -> list:
#     """Add custom column in queryset using pandas"""
#     if len(products) < 1:
#         return list()

#     df = pd.DataFrame(products)

#     df["is_authorized"] = df.apply(
#         lambda row: is_authorized_dealer(
#             Brand.objects.get(id=row["manufacturer"]), instance
#         ),
#         axis=1,
#     )

#     df["authorization_form_url"] = df.apply(
#         lambda row: Brand.objects.get(id=row["manufacturer"]).authorization_form_url,
#         axis=1,
#     )

#     data = json.loads(df.to_json(orient="records"))
#     return data


# class BrandViewSet(viewsets.ModelViewSet):
#     permission_classes = [AuthenticatedStaffOrReadOnly]
#     queryset = Brand.objects.all()
#     serializer_class = BrandSerializer
#     lookup_field = "uuid"  # Individual object will be found by this field

#     def perform_create(self, serializer, request):
#         serializer.save()

#     def perform_update(self, instance, serializer, request):
#         """Update an existing Brand and store activity log."""
#         previous_data_before_update = self.queryset.get(uuid=instance.uuid)
#         serializer.save()

#     def perform_destroy(self, instance, request):
#         serializer = self.serializer_class(instance).data
#         Product.objects.filter(manufacturer=instance).delete()
#         instance.delete()

#     def perform_soft_delete(self, instance, request):
#         instance.is_active = False
#         instance.is_soft_deleted = True
#         instance.save()
#         serializer = self.serializer_class(instance).data

#     def list(self, request, *args, **kwargs):
#         if not request.instance.is_staff:
#             category = request.GET.get("category", None)

#             # Customer request
#             queryset = self.get_queryset().filter(is_active=True, is_soft_deleted=False)
#             # inactive brand for dealer
#             inactive_brands_id = DealerBrand.objects.filter(
#                 dealer=request.instance, is_active=False
#             ).values_list("brand_id", flat=True)

#             # remove inactive brands for dealer
#             queryset = queryset.exclude(id__in=inactive_brands_id)

#             # brand filter based on category
#             if category:
#                 available_brands_of_selected_category = ProductCategory.objects.get(
#                     uuid=category
#                 ).brands.values_list("id", flat=True)

#                 queryset = queryset.filter(
#                     id__in=list(available_brands_of_selected_category)
#                 )
#         else:
#             # stuff request
#             queryset = self.get_queryset().filter(is_soft_deleted=False)
#         serializer = self.get_serializer(queryset, many=True).data
#         df = pd.DataFrame(serializer)
#         df["is_authorized"] = df.apply(
#             lambda row: is_authorized_dealer(
#                 Brand.objects.get(id=row["id"]), request.instance
#             ),
#             axis=1,
#         )

#         product_count_by_manufacturer_df = pd.DataFrame(
#             Product.objects.values("manufacturer__uuid").annotate(
#                 product_count=Count("manufacturer__uuid")
#             )
#         )

#         df = df.merge(
#             product_count_by_manufacturer_df,
#             how="left",
#             left_on="uuid",
#             right_on="manufacturer__uuid",
#         )
#         df["product_count"].fillna(0, inplace=True)
#         data = json.loads(df.to_json(orient="records"))
#         return Response({"data": data}, status=status.HTTP_200_OK)

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         files = request.FILES

#         # store files in server
#         for file in files:
#             file_path = f"{settings.BRAND_IMAGE_LOCATION}{files[file].name}"
#             path = default_storage.save(file_path, files[file])
#             data[file] = path

#         serializer = self.get_serializer(data=data)
#         if not serializer.is_valid():
#             return Response(
#                 {"details": serializer.errors},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         self.perform_create(serializer, request)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def update(self, request, *args, **kwargs):
#         data = request.data
#         files = request.FILES

#         # store files in server
#         for file in files:
#             file_path = ""
#             if file == "image":
#                 file_path = f"{settings.BRAND_IMAGE_LOCATION}{files[file].name}"
#             if file == "price_sheet_for_dealer":
#                 file_path = f"{settings.BRAND_PRICE_SHEET_FOR_DEALERS_LOCATION}{files[file].name}"
#             if file_path != "":
#                 path = default_storage.save(file_path, files[file])
#                 data[file] = path

#         instance = self.get_object()

#         serializer = self.get_serializer(instance, data=data, partial=True)
#         if not serializer.is_valid():
#             return Response(
#                 {"details": serializer.errors},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         self.perform_update(instance, serializer, request)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()  # get the requested object instance

#         # soft delete
#         if request.GET.get("sd", 0):
#             self.perform_soft_delete(instance, request)
#         else:
#             self.perform_destroy(instance, request)
#         return Response(
#             {"detail": "Brand deleted successfully"}, status=status.HTTP_200_OK
#         )

#     @action(detail=False, methods=["GET"], name="Sync Brand")
#     def sync_from_finale(self, request, *args, **kwargs):
#         # authenticate to finale inventory
#         try:
#             finale_inventory = FinaleInventory(
#                 settings.FINALE_URL,
#                 settings.FINALE_USERNAME,
#                 settings.FINALE_PASSWORD,
#             )

#             # request for manufacturer
#             response = finale_inventory.get_manufacturer_list(
#                 {
#                     "operationName": None,
#                     "variables": {},
#                     "query": '{ productMeta { filters(name: "manufacturer") { optionList { label value }}}}',
#                 }
#             )

#             if response["status"]:
#                 # successful response
#                 manufacturer_list = response["data"]

#                 manufacturer_objects = []
#                 all_brand_names_alphanum = [
#                     re.sub(r"[^A-Za-z0-9]", "", val).lower()
#                     for val in Brand.objects.values_list("name", flat=True)
#                 ]
#                 for manufacturer in manufacturer_list:
#                     manufacturer_name_alphanum = re.sub(
#                         r"[^A-Za-z0-9]", "", manufacturer["value"]
#                     ).lower()
#                     if manufacturer_name_alphanum not in all_brand_names_alphanum:
#                         manufacturer_objects.append(
#                             Brand(
#                                 uuid=random_hex_code(length=16),
#                                 name=manufacturer["value"],
#                                 created_by=request.instance.id,
#                                 updated_by=request.instance.id,
#                                 is_active=False,
#                             )
#                         )
#                 if len(manufacturer_objects):
#                     brands = Brand.objects.bulk_create(manufacturer_objects)
#                 return Response(
#                     {"details": "Brand synced successfully"}, status=status.HTTP_200_OK
#                 )
#             else:
#                 return Response(
#                     {"details": "Brand synced failed"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except Exception as ex:
#             return Response(
#                 {"details": ex.__str__()}, status=status.HTTP_400_BAD_REQUEST
#             )

#     @action(detail=False, methods=["GET"], name="Available Brand Page")
#     def available_brand_pages(self, request, *args, **kwargs):
#         queryset = Brand.objects.filter(is_brand_page_visible=True)
#         serializer = BrandSerializer(queryset, many=True)
#         return Response({"data": serializer.data}, status=status.HTTP_200_OK)

#     @action(detail=False, methods=["GET"], name="Search brand")
#     def search(self, request, *args, **kwargs):
#         query_param = self.request.GET.get("q")

#         if query_param == "":
#             return Response({"data": []}, status=status.HTTP_200_OK)

#         queryset = self.get_queryset().filter(
#             Q(name__icontains=query_param)
#             | Q(company_address__icontains=query_param)
#             | Q(company_email__icontains=query_param),
#             is_soft_deleted=False,
#         )

#         if not request.instance.is_staff:
#             queryset = queryset.filter(is_active=True)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response({"data": serializer.data}, status=status.HTTP_200_OK)


# class ProductCategoryViewSet(viewsets.ModelViewSet):
#     permission_classes = [AuthenticatedStaffOrReadOnly]
#     queryset = ProductCategory.objects.all()
#     serializer_class = ProductCategorySerializer
#     lookup_field = "uuid"  # Individual object will be found by this field

#     def perform_create(self, serializer, request):
#         serializer.save()

#     def perform_update(self, instance, serializer, request):
#         """Update an existing Brand and store activity log."""
#         previous_data_before_update = self.queryset.get(uuid=instance.uuid)
#         serializer.save()

#     def perform_destroy(self, instance, request):
#         serializer = self.serializer_class(instance).data
#         instance.delete()

#     def perform_soft_delete(self, instance, request):
#         instance.is_active = False
#         instance.is_soft_deleted = True
#         instance.save()
#         serializer = self.serializer_class(instance).data

#     def list(self, request, *args, **kwargs):
#         if not request.instance.is_staff:
#             # Customer request
#             queryset = self.get_queryset().filter(is_active=True, is_soft_deleted=False)
#         else:
#             # stuff request
#             queryset = self.get_queryset().filter(is_soft_deleted=False)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response({"data": serializer.data}, status=status.HTTP_200_OK)

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         files = request.FILES

#         # store files in server
#         for file in files:
#             file_path = f"{settings.CATEGORY_IMAGE_LOCATION}{files[file].name}"
#             path = default_storage.save(file_path, files[file])
#             data[file] = path

#         serializer = self.get_serializer(data=data)
#         if not serializer.is_valid():
#             return Response(
#                 {"details": serializer.errors},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         self.perform_create(serializer, request)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def update(self, request, *args, **kwargs):
#         data = request.data
#         files = request.FILES

#         # store files in server
#         for file in files:
#             file_path = f"{settings.CATEGORY_IMAGE_LOCATION}{files[file].name}"
#             path = default_storage.save(file_path, files[file])
#             data[file] = path

#         instance = self.get_object()

#         serializer = self.get_serializer(instance, data=data, partial=True)
#         if not serializer.is_valid():
#             return Response(
#                 {"details": serializer.errors},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         self.perform_update(instance, serializer, request)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()  # get the requested object instance

#         # soft delete
#         if request.GET.get("sd", 0):
#             self.perform_soft_delete(instance, request)
#         else:
#             self.perform_destroy(instance, request)
#         return Response(
#             {"detail": "ProductCategory deleted successfully"},
#             status=status.HTTP_200_OK,
#         )

#     @action(detail=False, methods=["GET"], name="Sync Product Category")
#     def sync_from_finale(self, request, *args, **kwargs):
#         # authenticate to finale inventory
#         try:
#             finale_inventory = FinaleInventory(
#                 settings.FINALE_URL,
#                 settings.FINALE_USERNAME,
#                 settings.FINALE_PASSWORD,
#             )

#             # request for product category
#             response = finale_inventory.get_product_category_list()

#             if response["status"]:
#                 # successful response
#                 product_category_list = response["data"]

#                 product_category_objects = []
#                 for product_category in product_category_list:
#                     if not ProductCategory.objects.filter(
#                         finale_name=product_category["label"]
#                     ).exists():
#                         product_category_objects.append(
#                             ProductCategory(
#                                 uuid=random_hex_code(length=16),
#                                 name=product_category["label"],
#                                 finale_name=product_category["label"],
#                                 created_by=request.instance.id,
#                                 updated_by=request.instance.id,
#                             )
#                         )
#                 if len(product_category_objects):
#                     product_categories = ProductCategory.objects.bulk_create(
#                         product_category_objects
#                     )
#                 return Response(
#                     {"details": "Brand synced successfully"}, status=status.HTTP_200_OK
#                 )
#             else:
#                 return Response(
#                     {"details": "ProductCategory synced failed"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except Exception as ex:
#             return Response(
#                 {"details": ex.__str__()}, status=status.HTTP_400_BAD_REQUEST
#             )


# class SupplierViewSet(viewsets.ModelViewSet):
#     permission_classes = [AuthenticatedStaffOrReadOnly]
#     queryset = Supplier.objects.all()
#     serializer_class = SupplierSerializer
#     lookup_field = "uuid"  # Individual object will be found by this field

#     def perform_create(self, serializer, request):
#         serializer.save()

#     def perform_update(self, instance, serializer, request):
#         """Update an existing Supplier and store activity log."""
#         previous_data_before_update = self.queryset.get(uuid=instance.uuid)
#         serializer.save()

#     def perform_destroy(self, instance, request):
#         serializer = self.serializer_class(instance).data
#         instance.delete()

#     def perform_soft_delete(self, instance, request):
#         instance.is_active = False
#         instance.is_soft_deleted = True
#         instance.save()
#         serializer = self.serializer_class(instance).data

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset().filter(is_soft_deleted=False)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response({"data": serializer.data}, status=status.HTTP_200_OK)

#     def create(self, request, *args, **kwargs):
#         data = request.data

#         serializer = self.get_serializer(data=data)
#         if not serializer.is_valid():
#             return Response(
#                 {"details": serializer.errors},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         self.perform_create(serializer, request)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def update(self, request, *args, **kwargs):
#         data = request.data

#         instance = self.get_object()

#         serializer = self.get_serializer(instance, data=data, partial=True)
#         if not serializer.is_valid():
#             return Response(
#                 {"details": serializer.errors},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         self.perform_update(instance, serializer, request)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()  # get the requested object instance

#         # soft delete
#         if request.GET.get("sd", 0):
#             self.perform_soft_delete(instance, request)
#         else:
#             self.perform_destroy(instance, request)
#         return Response(
#             {"detail": "Supplier deleted successfully"}, status=status.HTTP_200_OK
#         )

#     @action(detail=False, methods=["GET"], name="Sync Supplier")
#     def sync_from_finale(self, request, *args, **kwargs):
#         # authenticate to finale inventory
#         try:
#             finale_inventory = FinaleInventory(
#                 settings.FINALE_URL,
#                 settings.FINALE_USERNAME,
#                 settings.FINALE_PASSWORD,
#             )

#             # request for supplier
#             response = finale_inventory.get_supplier_list(
#                 {
#                     "operationName": None,
#                     "variables": {},
#                     "query": "query Rows($search: String, $after: String, "
#                     "$first: Int) { partyViewConnection(role: "
#                     '["SUPPLIER"], status: ["PARTY_ENABLED", '
#                     '"PARTY_DISABLED"], search: $search, '
#                     "after: $after, first: $first) { edges { node "
#                     "{ partyId partyUrl name status }} pageInfo {"
#                     "hasNextPage endCursor }}}",
#                 }
#             )

#             if response["status"]:
#                 # successful response
#                 supplier_list = response["data"]

#                 supplier_objects_create, supplier_objects_update = [], []
#                 for supplier in supplier_list:
#                     if (
#                         supplier["node"]["name"] != ""
#                         and supplier["node"]["name"] is not None
#                         and not Supplier.objects.filter(
#                             finale_id=supplier["node"]["partyId"]
#                         ).exists()
#                     ):
#                         is_active = (
#                             True if supplier["node"]["status"] == "Active" else False
#                         )
#                         supplier_objects_create.append(
#                             Supplier(
#                                 uuid=random_hex_code(length=16),
#                                 name=supplier["node"]["name"],
#                                 finale_id=supplier["node"]["partyId"],
#                                 finale_detail_url=supplier["node"]["partyUrl"],
#                                 is_active=is_active,
#                                 created_by=request.instance.id,
#                                 updated_by=request.instance.id,
#                             )
#                         )
#                     if (
#                         supplier["node"]["name"] != ""
#                         and supplier["node"]["name"] is not None
#                         and Supplier.objects.filter(
#                             finale_id=supplier["node"]["partyId"]
#                         ).exists()
#                     ):
#                         is_active = (
#                             True if supplier["node"]["status"] == "Active" else False
#                         )
#                         if (
#                             Supplier.objects.get(
#                                 finale_id=supplier["node"]["partyId"]
#                             ).is_active
#                             != is_active
#                         ):
#                             updated_object = Supplier.objects.get(
#                                 finale_id=supplier["node"]["partyId"]
#                             )
#                             updated_object.name = supplier["node"]["name"]
#                             updated_object.is_active = is_active
#                             updated_object.updated_by = request.instance.id
#                             supplier_objects_update.append(updated_object)

#                 if len(supplier_objects_create):
#                     suppliers = Supplier.objects.bulk_create(supplier_objects_create)

#                 if len(supplier_objects_update):
#                     update_suppliers = Supplier.objects.bulk_update(
#                         supplier_objects_update, ["name", "is_active", "updated_by"]
#                     )
#                 return Response(
#                     {"details": "Supplier synced successfully"},
#                     status=status.HTTP_200_OK,
#                 )
#             else:
#                 return Response(
#                     {"details": "Supplier synced failed"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except Exception as ex:
#             return Response(
#                 {"details": ex.__str__()}, status=status.HTTP_400_BAD_REQUEST
#             )


# class DealerBrandViewSet(viewsets.ModelViewSet):
#     permission_classes = [AuthenticatedStaffOrReadOnly]
#     queryset = DealerBrand.objects.all()
#     serializer_class = DealerBrandSerializer
#     lookup_field = "uuid"  # Individual object will be found by this field

#     def list(self, request, *args, **kwargs):
#         brand_uuid = self.request.GET.get("brand")
#         dealer_uuid = self.request.GET.get("dealer")

#         if brand_uuid and dealer_uuid:
#             # return only a specific brands details
#             queryset = self.get_queryset().filter(
#                 dealer__uuid=dealer_uuid,
#                 brand__uuid=brand_uuid,
#                 is_soft_deleted=False,
#             )
#             serializer = self.get_serializer(queryset, many=True)
#             return Response({"data": serializer.data}, status=status.HTTP_200_OK)

#         if not request.instance.is_staff:
#             # Customer request
#             queryset = self.get_queryset().filter(is_active=True, is_soft_deleted=False)
#         else:
#             # stuff request
#             queryset = self.get_queryset().filter(is_soft_deleted=False)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response({"data": serializer.data}, status=status.HTTP_200_OK)

#     def create(self, request, *args, **kwargs):
#         instance = None
#         data = request.data

#         queryset = DealerBrand.objects.filter(
#             brand__uuid=data.get("brand"), dealer__uuid=data.get("dealer")
#         )

#         if queryset.exists():
#             instance = queryset[0]
#             instance.discount = data.get("discount")
#             instance.is_authorized = True if data.get("is_authorized") == "1" else False
#             instance.is_active = True if data.get("is_active") == "1" else False
#             instance.save()
#         else:
#             instance = DealerBrand.objects.create(
#                 brand=Brand.objects.get(uuid=data.get("brand")),
#                 dealer=User.objects.get(uuid=data.get("dealer")),
#                 discount=data.get("discount"),
#                 is_active=True if data.get("is_active") == "1" else False,
#             )
#             instance.save()
#         return Response(
#             DealerBrandSerializer(instance).data, status=status.HTTP_201_CREATED
#         )


# class BrandPageImageViewSet(BaseGenericAPIView):
#     permission_classes = [AuthenticatedStaffOrReadOnly]
#     pagination_class = LargeResultsSetPagination
#     model = BrandPageImage
#     queryset = BrandPageImage.objects.all()
#     serializer_class = BrandPageImageSerializer
#     lookup_field = "uuid"  # Individual object will be found by this field
#     search_keywords = ["title", "image"]

#     def perform_create(self, serializer, request):
#         serializer.save()

#     def perform_update(self, instance, serializer, request):
#         """Update an existing Brand and store activity log."""
#         previous_data_before_update = self.queryset.get(uuid=instance.uuid)
#         serializer.save()

#     def perform_destroy(self, instance, request):
#         serializer = self.serializer_class(instance).data
#         instance.delete()

#     def list(self, request, *args, **kwargs):
#         return Response({"data": []}, status=status.HTTP_200_OK)

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         files = request.FILES.getlist("image")

#         brand_uuid = data.get("brand")
#         if brand_uuid:
#             brand = Brand.objects.get(uuid=brand_uuid)
#             data["brand"] = brand.id

#         # store files in server
#         for file in files:
#             file_path = f"{settings.BRAND_PAGE_IMAGE_LOCATION}{file.name}"
#             path = default_storage.save(file_path, file)
#             data["image"] = path

#             serializer = self.get_serializer(data=data)
#             if not serializer.is_valid():
#                 return Response(
#                     {"details": serializer.errors},
#                     status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                 )

#             self.perform_create(serializer, request)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def update(self, request, *args, **kwargs):
#         data = request.data
#         files = request.FILES

#         # store files in server
#         for file in files:
#             file_path = f"{settings.BRAND_PAGE_IMAGE_LOCATION}{files[file].name}"
#             path = default_storage.save(file_path, files[file])
#             data[file] = path

#         instance = self.get_object()

#         serializer = self.get_serializer(instance, data=data, partial=True)
#         if not serializer.is_valid():
#             return Response(
#                 {"details": serializer.errors},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         self.perform_update(instance, serializer, request)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()  # get the requested object instance
#         self.perform_destroy(instance, request)
#         return Response(
#             {"detail": "BrandPageImage deleted successfully"}, status=status.HTTP_200_OK
#         )

#     @action(detail=False, methods=["GET"], name="Brand Page")
#     def page_wise_images(self, request, *args, **kwargs):
#         brand_uuid = request.query_params.get("brand")

#         data = BrandPageImage.objects.filter(
#             is_active=True, brand__uuid=brand_uuid
#         )

#         if not request.instance.is_staff:
#             data = data.filter(brand__is_brand_page_visible=True)
#         data = data.order_by("order")

#         serializer = BrandPageImageSerializer(data, many=True)
#         if data.exists():
#             data = {
#                 "name": data.first().brand.name,
#                 "email": data.first().brand.company_email,
#                 "tagline": data.first().brand.tagline,
#                 "url": data.first().brand.company_url,
#                 "data": serializer.data,
#             }
#         return Response({"data": data})


# @api_view(["GET"])
# def get_advanced_search_data(request):
#     data = dict()
#     years = [str(2026 - year) for year in range(1, 99)]

#     # authorized brands
#     brands = Brand.objects.filter(is_active=True, is_soft_deleted=False)
#     # inactive brand for dealer
#     inactive_brands_id = DealerBrand.objects.filter(
#         dealer=request.instance, is_active=False
#     ).values_list("brand_id", flat=True)
#     # remove inactive brands for dealer
#     brands = list(
#         brands.exclude(id__in=inactive_brands_id)
#         .values("uuid", "name")
#         .order_by("name")
#     )

#     models = Brand.objects.filter(is_active=True)

#     data["years"] = []
#     data["brands"] = brands
#     data["models"] = []
#     return Response({"data": data})


# class FilesViewSet(BaseGenericAPIView):
#     permission_classes = [AuthenticatedStaffOrReadOnly]
#     pagination_class = LargeResultsSetPagination
#     model = Files
#     queryset = Files.objects.all()
#     serializer_class = FilesSerializer
#     lookup_field = "uuid"  # Individual object will be found by this field
#     search_keywords = ["file", "type", "instance__name", "instance__email"]

#     def perform_create(self, serializer, request):
#         serializer.save()

#     def perform_update(self, instance, serializer, request):
#         """Update an existing Files and store activity log."""
#         previous_data_before_update = self.queryset.get(uuid=instance.uuid)
#         serializer.save()

#     def perform_destroy(self, instance, request):
#         serializer = self.serializer_class(instance).data
#         instance.delete()

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset().order_by("-id")
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True).data
#             return self.get_paginated_response(serializer)

#         serializer = self.get_serializer(queryset, many=True).data
#         return Response({"data": serializer}, status=status.HTTP_200_OK)

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         files = self.request.FILES.getlist("files")

#         # store files in server
#         for file in files:
#             try:
#                 file_path = f"{settings.FILES_LOCATION}{time.time()}.{file.name}"
#                 path = default_storage.save(file_path, file)
#                 data["file"] = path
#                 data["is_active"] = True
#                 if data.get("instance", "null") == "null":
#                     data.pop("instance")
#                 serializer = self.get_serializer(data=data)
#                 if not serializer.is_valid():
#                     return Response(
#                         {"details": serializer.errors},
#                         status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                     )

#                 self.perform_create(serializer, request)
#                 if data.get("is_encrypted", "true") == "true":
#                     path = Path(f"{settings.BASE_DIR}/media/{file_path}")
#                     Encryption().file_encrypt(path, f"{path}.enc")
#                     Path(path).unlink()
#             except Exception as ex:
#                 logging.getLogger("warning_logger").warning(ex.__str__())
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def update(self, request, *args, **kwargs):
#         pass

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()  # get the requested object instance
#         self.perform_destroy(instance, request)
#         return Response(
#             {"detail": "File deleted successfully"}, status=status.HTTP_200_OK
#         )

#     @action(detail=False, methods=["POST"], name="Encrypt File")
#     def encrypt(self, request, *args, **kwargs):
#         data = self.request.data
#         path = Path(f"{settings.BASE_DIR}/media/{data.get('file_path')}")

#         if data.get("file_path") and path.exists() and path.is_file():
#             Encryption().file_encrypt(path, f"{path}.enc")
#             Path(path).unlink()

#             try:
#                 self.model.objects.filter(file=f"{data.get('file_path')}").update(
#                     is_encrypted=True
#                 )
#             except Exception as ex:
#                 pass
#             return Response({"data": "Encrypted"}, status=status.HTTP_200_OK)
#         return Response({"data": "Failed"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

#     @action(detail=False, methods=["POST"], name="Decrypt File")
#     def decrypt(self, request, *args, **kwargs):
#         data = self.request.data
#         path = Path(f"{settings.BASE_DIR}/media/{data.get('file_path')}.enc")

#         if data.get("file_path") and path.exists() and path.is_file():
#             Encryption().file_decrypt(path, f"{path}"[:-4])
#             Path(path).unlink()

#             try:
#                 self.model.objects.filter(file=f"{data.get('file_path')}").update(
#                     is_encrypted=False
#                 )
#             except Exception as ex:
#                 pass
#             return Response({"data": "Decrypted"}, status=status.HTTP_200_OK)
#         return Response({"data": "Failed"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


# class warehouseViewSet(viewsets.ModelViewSet):
#     permission_classes = [AuthenticatedStaffOrReadOnly]
#     queryset = warehouse.objects.all()
#     serializer_class = warehouseSerializer
#     lookup_field = "uuid"  # Individual object will be found by this field

#     def perform_create(self, serializer, request):
#         serializer.save()

#     def perform_update(self, instance, serializer, request):
#         """Update an existing warehouse and store activity log."""
#         previous_data_before_update = self.queryset.get(uuid=instance.uuid)
#         serializer.save()

#     def perform_destroy(self, instance, request):
#         serializer = self.serializer_class(instance).data
#         instance.delete()

#     def perform_soft_delete(self, instance, request):
#         instance.is_active = False
#         instance.is_soft_deleted = True
#         instance.save()
#         serializer = self.serializer_class(instance).data

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset().filter(is_soft_deleted=False)
#         if request.GET.get("term"):
#             queryset = queryset.filter(name__icontains=request.GET.get("term"))
#         serializer = self.get_serializer(queryset, many=True)
#         return Response({"data": serializer.data}, status=status.HTTP_200_OK)

#     def create(self, request, *args, **kwargs):
#         data = request.data

#         serializer = self.get_serializer(data=data)
#         if not serializer.is_valid():
#             return Response(
#                 {"details": serializer.errors},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         self.perform_create(serializer, request)
#         self.update_price_sheet_template()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def update(self, request, *args, **kwargs):
#         data = request.data

#         instance = self.get_object()

#         serializer = self.get_serializer(instance, data=data, partial=True)
#         if not serializer.is_valid():
#             return Response(
#                 {"details": serializer.errors},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         self.perform_update(instance, serializer, request)
#         self.update_price_sheet_template()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()  # get the requested object instance

#         # soft delete
#         if request.GET.get("sd", 0):
#             self.perform_soft_delete(instance, request)
#         else:
#             self.perform_destroy(instance, request)
#         self.update_price_sheet_template()
#         return Response(
#             {"detail": "warehouse deleted successfully"}, status=status.HTTP_200_OK
#         )

#     @staticmethod
#     def update_price_sheet_template():
#         # update price sheet csv column for warehouses
#         price_sheet = f"{settings.BASE_DIR}/apps/admin/admin_inventory/static/downloadable/upload_price_sheet_template.csv"
#         price_sheet_df = pd.read_csv(price_sheet)
#         available_columns = list(price_sheet_df.columns)
#         new_columns = []
#         warehouses = [
#             f"WAREHOUSE {warehouse}"
#             for warehouse in warehouse.objects.filter(is_active=True).values_list(
#                 "name", flat=True
#             )
#         ]

#         # remove all columns from price sheet df
#         [price_sheet_df.pop(column) for column in available_columns]

#         # remove all warehouse columns from csv
#         [
#             new_columns.append(warehouse)
#             for warehouse in available_columns
#             if not warehouse.startswith("WAREHOUSE ")
#         ]

#         new_columns += warehouses

#         # insert all columns to price sheet df
#         [
#             price_sheet_df.insert(i, column, "", False)
#             for i, column in enumerate(new_columns)
#         ]

#         # save new csv
#         price_sheet_df.to_csv(price_sheet, index=False)

#         # run collectstatic for update in static forlder
#         call_command("collectstatic", "--no-input")

#     @action(detail=False, methods=["GET"], name="Product List")
#     def product(self, request, *args, **kwargs):
#         query_param = self.request.GET.get("warehouse")

#         if query_param == "":
#             return Response({"data": []}, status=status.HTTP_200_OK)

#         queryset = ProductInwarehouse.objects.filter(warehouse__uuid=query_param)

#         serializer = ProductInwarehouseSerializer(queryset, many=True)
#         return Response({"data": serializer.data}, status=status.HTTP_200_OK)


# class ProductInwarehouseViewSet(viewsets.ModelViewSet):
#     permission_classes = [AuthenticatedStaffOrReadOnly]
#     queryset = ProductInwarehouse.objects.all()
#     serializer_class = ProductInwarehouseSerializer
#     lookup_field = "uuid"  # Individual object will be found by this field

#     def perform_create(self, serializer, request):
#         serializer.save()

#     def perform_update(self, instance, serializer, request):
#         """Update an existing ProductInwarehouse and store activity log."""
#         previous_data_before_update = self.queryset.get(uuid=instance.uuid)
#         instance.stock = request.data["stock"]
#         instance.save()

#     def perform_destroy(self, instance, request):
#         serializer = self.serializer_class(instance).data
#         instance.delete()

#     def perform_soft_delete(self, instance, request):
#         instance.is_active = False
#         instance.is_soft_deleted = True
#         instance.save()
#         serializer = self.serializer_class(instance).data

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset().filter(is_soft_deleted=False)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response({"data": serializer.data}, status=status.HTTP_200_OK)

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         validate_data = {
#             "product": Product.objects.get(uuid=data["product"]).id,
#             "warehouse": warehouse.objects.get(uuid=data["warehouse"]).id,
#             "stock": data["stock"],
#         }

#         serializer = self.get_serializer(data=validate_data)
#         if not serializer.is_valid():
#             return Response(
#                 {"details": serializer.errors},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         if not ProductInwarehouse.objects.filter(
#             product__uuid=data["product"], warehouse__uuid=data["warehouse"]
#         ).exists():
#             self.perform_create(serializer, request)
#         else:
#             instance = ProductInwarehouse.objects.get(
#                 product__uuid=data["product"],
#                 warehouse__uuid=data["warehouse"],
#             )
#             self.perform_update(instance, serializer, request)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def update(self, request, *args, **kwargs):
#         pass

#     def destroy(self, request, *args, **kwargs):
#         pass


# # make an endpoint
# class StockTransactionViewSet(BaseGenericAPIView):
#     permission_classes = [AuthenticatedStaffOrReadOnly]
#     pagination_class = LargeResultsSetPagination
#     model = StockTransaction
#     queryset = StockTransaction.objects.all()
#     serializer_class = StockTransactionSerializer
#     lookup_field = "uuid"  # Individual object will be found by this field
#     search_keywords = [
#         "product__part_no",
#         "product__product_id",
#         "po__number",
#         "so__number",
#     ]

#     def perform_create(self, serializer, request):
#         serializer.save()

#     def perform_update(self, instance, serializer, request):
#         """Update an existing StockTransaction and store activity log."""
#         previous_data_before_update = self.queryset.get(uuid=instance.uuid)
#         instance.stock = request.data["stock"]
#         instance.save()

#     def perform_destroy(self, instance, request):
#         serializer = self.serializer_class(instance).data
#         instance.delete()

#     def perform_soft_delete(self, instance, request):
#         instance.is_active = False
#         instance.is_soft_deleted = True
#         instance.save()
#         serializer = self.serializer_class(instance).data

#     @staticmethod
#     def string_to_datetime_object(str_date):
#         return datetime.datetime.strptime(str_date, "%m/%d/%Y")

#     def filter(self, queryset, **kwargs):
#         """
#         data = {
#             "transaction_type": 2,
#             "date_range": "12/01/2022 - 12/31/2022"
#         }
#         """
#         # single transaction type only
#         if kwargs.get("transaction_type") not in ["0", 0, "", None]:
#             queryset = queryset.filter(transaction_type=kwargs.get("transaction_type"))

#         # date range filter
#         if kwargs.get("date_range") not in ["", None]:
#             _from, _to = kwargs.get("date_range").split(" - ")
#             queryset = queryset.filter(
#                 created_at__range=[
#                     self.string_to_datetime_object(_from),
#                     self.string_to_datetime_object(_to) + datetime.timedelta(days=1),
#                 ]
#             )

#         return queryset

#     def list(self, request, *args, **kwargs):
#         data = {
#             "transaction_type": request.GET.get("transaction_type", 0),
#             "date_range": request.GET.get("date_range", "01/01/2020 - 12/31/2099"),
#         }
#         queryset = self.get_queryset().filter(is_soft_deleted=False)

#         queryset = self.filter(queryset=queryset, **data)

#         count_product = queryset.values("product__product_id").annotate(
#             product__product_id__count=Sum(
#                 F("purchase_stock") + F("sell_stock"), output_field=FloatField()
#             )
#         )

#         prices = {
#             "purchase": queryset.aggregate(aggr_amount=Sum("purchase_amount"))["aggr_amount"],
#             "sell": queryset.aggregate(aggr_amount=Sum("sell_amount"))["aggr_amount"],
#             "sell_profit": queryset.aggregate(aggr_amount=Sum("sell_amount_profit"))["aggr_amount"],
#         }

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             self.set_paginated_kwargs(
#                 **{"count_product": count_product, "prices": prices}
#             )
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(
#             {"data": serializer.data, "count_product": count_product},
#             status=status.HTTP_200_OK,
#         )

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         logging.getLogger("warning_logger").warning("=================================")
#         logging.getLogger("warning_logger").warning("New Transaction Request Received")
#         logging.getLogger("warning_logger").warning(json.dumps(data))

#         # collect request params
#         validate_data = {
#             "id": data.get("id", None),  # product id
#             "uuid": data.get("uuid", None),  # so/po hashed id
#             "unit_price": data.get("unit_price", None),
#             "product_id": data.get("product_id", None),
#             "warehouses": data.get("warehouses", None),
#         }

#         # verify required params
#         # check transaction type
#         if data.get("current_delivered", None):
#             # SO (SALES ORDER) transaction
#             validate_data["current_delivered"] = data.get("current_delivered", None)
#         elif data.get("current_received", None):
#             # PO (PURCHASE ORDER) transaction
#             validate_data["current_received"] = data.get("current_received", None)
#         elif data.get("current_invoiced", None):
#             # INVOICED transaction
#             validate_data["current_invoiced"] = data.get("current_invoiced", None)
#         else:
#             # INVALID transaction
#             return Response(
#                 {"details": "Invalid transaction type"},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         # check requested params are valid for transaction
#         # transaction data must not contain any None/null value
#         # dummy request format:
#         # {
#         #   "product_id": "SPF200K",
#         #   "current_delivered": "01",
#         #   "uuid": "9801ad0316aa4f80", #so/po
#         #   "warehouses": [
#         #       {
#         #           "id": 2,
#         #           "uuid": "0f83e378c6a84044",
#         #           "stock": "01"
#         #       },
#         #       {
#         #           "id": 4,
#         #           "uuid": "1ced3514cc1248e7",
#         #           "stock": "0"
#         #       }
#         #   ]
#         # }
#         if None in validate_data.values():
#             return Response(
#                 {"details": "Invalid transaction data"},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         # validate warehouse data with proper key value
#         for warehouse in validate_data["warehouses"]:
#             if sorted(list(warehouse.keys())) != sorted(["id", "uuid", "stock"]):
#                 return Response(
#                     {"details": "Invalid transaction warehouse data"},
#                     status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                 )

#         # make atomic transaction
#         try:
#             with transaction.atomic():
#                 product = Product.objects.get(id=validate_data["id"])

#                 if data.get("current_received", None):

#                     # update product (done at stock_transaction.py here we are just validating stock)
#                     try:
#                         current_stock = float(product.stock) + float(
#                             validate_data["current_received"]
#                         )
#                     except Exception as ex:
#                         current_stock = float(validate_data["current_received"])

#                     if current_stock < 0:
#                         error = f"Insufficient product in stock."
#                         logging.getLogger("warning_logger").warning(error)
#                         return Response(
#                             {"details": {0: [error]}},
#                             status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                         )

#                     # update po
#                     po = PurchaseOrder.objects.get(uuid=validate_data["uuid"])
#                     original_products = copy.deepcopy(po.data["products"])
#                     temp_products = po.data["products"]
#                     _temp_products = []

#                     for temp_product in temp_products:
#                         if temp_product["uuid"] == product.uuid:
#                             # deduct stock as this is a PO transaction
#                             current_stock = float(temp_product["pending"]) - float(
#                                 validate_data["current_received"]
#                             )

#                             if current_stock < 0:
#                                 error = f"Insufficient stock at warehouse"
#                                 logging.getLogger("warning_logger").warning(error)
#                                 return Response(
#                                     {"details": {0: [error]}},
#                                     status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                                 )

#                             temp_product["pending"] = current_stock
#                             temp_product["received"] = (
#                                 float(temp_product["quantity"]) - current_stock
#                             )

#                         _temp_products.append(temp_product)
#                     # update po product stocks
#                     po.data["products"] = _temp_products
#                     po.is_stock_updated = True
#                     po.save()
#                     logging.getLogger("warning_logger").warning("PO")
#                     logging.getLogger("warning_logger").warning(
#                         PurchaseOrderSerializer(po).data
#                     )

#                     # update warehouse
#                     # check product in warehouse
#                     for warehouse in validate_data["warehouses"]:
#                         if warehouse["stock"] not in ["", 0, "0", None]:
#                             product_in_warehouse = (
#                                 ProductInwarehouse.objects.get_or_create(
#                                     product=Product.objects.get(id=validate_data["id"]),
#                                     warehouse=warehouse.objects.get(id=warehouse["id"]),
#                                 )
#                             )

#                             product_in_warehouse = ProductInwarehouse.objects.get(
#                                 product_id=validate_data["id"],
#                                 warehouse_id=warehouse["id"],
#                             )

#                             # add stock as this is a PO transaction
#                             current_stock = float(product_in_warehouse.stock) + float(
#                                 warehouse["stock"]
#                             )

#                             if current_stock < 0:
#                                 error = f"Insufficient stock at warehouse '{product_in_warehouse.warehouse.name}'"
#                                 logging.getLogger("warning_logger").warning(error)
#                                 return Response(
#                                     {"details": {0: [error]}},
#                                     status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                                 )

#                             # TODO: stop processing all input before 2022-04-01
#                             if (
#                                 po.date
#                                 >= datetime.datetime.strptime(
#                                     "2022-04-01", "%Y-%m-%d"
#                                 ).date()
#                             ):
#                                 product_in_warehouse.stock = str(current_stock)
#                                 product_in_warehouse.save()
#                                 logging.getLogger("warning_logger").warning(
#                                     "PRODUCT IN WAREHOUSE"
#                                 )
#                                 logging.getLogger("warning_logger").warning(
#                                     ProductInwarehouseSerializer(
#                                         product_in_warehouse
#                                     ).data
#                                 )

#                     # make a transaction
#                     _transaction = Transaction(
#                         transaction_type=1,
#                         product=product,
#                         po=po,
#                         so=None,
#                         io=None,
#                         discount=float(po.data["discount"]),
#                         delivery_cost=float(po.data.get("discount", 0)),
#                         notes="",
#                         purchase_stock=float(validate_data["current_received"]),
#                         purchase_unit_price=float(validate_data["unit_price"]),
#                         purchase_amount=float(validate_data["current_received"])
#                         * float(validate_data["unit_price"]),
#                         sell_stock=0,
#                         sell_unit_price=0,
#                         sell_amount=0,
#                     )
#                     _transaction.calculation()

#                 elif data.get("current_delivered", None):

#                     # update product (done at stock_transaction.py here we are just validating stock)
#                     try:
#                         current_stock = float(product.stock) - float(
#                             validate_data["current_delivered"]
#                         )
#                     except Exception as ex:
#                         current_stock = float(validate_data["current_delivered"])
#                     if current_stock < 0:
#                         error = f"Insufficient product in stock."
#                         logging.getLogger("warning_logger").warning(error)
#                         return Response(
#                             {"details": {0: [error]}},
#                             status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                         )

#                     # update so
#                     so = SalesOrder.objects.get(uuid=validate_data["uuid"])
#                     original_products = copy.deepcopy(so.data["products"])
#                     temp_products = so.data["products"]
#                     _temp_products = []

#                     for temp_product in temp_products:
#                         if temp_product["uuid"] == product.uuid:
#                             # deduct stock as this is a SO transaction
#                             current_stock = float(temp_product["pending"]) - float(
#                                 validate_data["current_delivered"]
#                             )

#                             if current_stock < 0:
#                                 error = f"Insufficient stock at warehouse"
#                                 logging.getLogger("warning_logger").warning(error)
#                                 return Response(
#                                     {"details": {0: [error]}},
#                                     status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                                 )

#                             temp_product["pending"] = current_stock
#                             temp_product["delivered"] = (
#                                 float(temp_product["quantity"]) - current_stock
#                             )

#                         _temp_products.append(temp_product)
#                     # update so product stocks
#                     so.data["products"] = _temp_products
#                     so.is_stock_updated = True
#                     so.is_quotation = False  # this is no more a quotation
#                     so.save()
#                     logging.getLogger("warning_logger").warning("SO")
#                     logging.getLogger("warning_logger").warning(
#                         SalesOrderSerializer(so).data
#                     )

#                     # update warehouse
#                     # check product in warehouse
#                     for warehouse in validate_data["warehouses"]:
#                         if warehouse["stock"] not in ["", 0, "0", None]:
#                             product_in_warehouse = (
#                                 ProductInwarehouse.objects.get_or_create(
#                                     product=Product.objects.get(id=validate_data["id"]),
#                                     warehouse=warehouse.objects.get(id=warehouse["id"]),
#                                 )
#                             )

#                             product_in_warehouse = ProductInwarehouse.objects.get(
#                                 product_id=validate_data["id"],
#                                 warehouse_id=warehouse["id"],
#                             )

#                             # deduct stock as this is a SO transaction
#                             current_stock = float(product_in_warehouse.stock) - float(
#                                 warehouse["stock"]
#                             )

#                             if current_stock < 0:
#                                 error = f"Insufficient stock at warehouse '{product_in_warehouse.warehouse.name}'"
#                                 logging.getLogger("warning_logger").warning(error)
#                                 return Response(
#                                     {"details": {0: [error]}},
#                                     status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                                 )

#                             product_in_warehouse.stock = str(current_stock)

#                             # TODO: stop processing all input before 2022-04-01
#                             if (
#                                 so.date
#                                 >= datetime.datetime.strptime(
#                                     "2022-04-01", "%Y-%m-%d"
#                                 ).date()
#                             ):
#                                 product_in_warehouse.save()
#                                 logging.getLogger("warning_logger").warning(
#                                     "PRODUCT IN WAREHOUSE"
#                                 )
#                                 logging.getLogger("warning_logger").warning(
#                                     ProductInwarehouseSerializer(
#                                         product_in_warehouse
#                                     ).data
#                                 )

#                     # make a transaction
#                     _transaction = Transaction(
#                         transaction_type=2,
#                         product=product,
#                         po=None,
#                         so=so,
#                         io=None,
#                         discount=float(so.data["discount"]),
#                         delivery_cost=float(so.data.get("discount", 0)),
#                         notes="",
#                         purchase_stock=0,
#                         purchase_unit_price=0,
#                         purchase_amount=0,
#                         sell_stock=float(validate_data["current_delivered"]),
#                         sell_unit_price=float(validate_data["unit_price"]),
#                         sell_amount=float(validate_data["current_delivered"])
#                         * float(validate_data["unit_price"]),
#                     )
#                     if not so.is_dropship:
#                         # dropship transactions will not impact on stock
#                         _transaction.calculation()

#                 else:
#                     invoice = data.get("current_received", None)
#         except Exception as ex:
#             logging.getLogger("warning_logger").warning(ex.__str__())
#             return Response(
#                 {"details": ex.__str__()}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
#             )

#         serializer = self.get_serializer(_transaction)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def update(self, request, *args, **kwargs):
#         pass

#     def destroy(self, request, *args, **kwargs):
#         pass


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_products(request):
#     created_at = request.GET.get("created_at")
#     updated_at = request.GET.get("updated_at")

#     if created_at:
#         products = Product.objects.filter(
#             created_at__date=created_at, is_soft_deleted=False
#         )
#     elif updated_at:
#         products = Product.objects.filter(
#             updated_at__date=updated_at, is_soft_deleted=False
#         )
#     else:
#         products = Product.objects.filter(id=0)

#     paginator = CustomResultsSetPageWisePagination()
#     page = paginator.paginate_queryset(products, request)
#     serializer = ProductOutputSerializer(page, many=True, context={"request": request})
#     return paginator.get_paginated_response(serializer.data)


# class ProductAttributeTypeViewSet(BaseGenericAPIView):
#     permission_classes = [AuthenticatedStaffOrReadOnly]
#     pagination_class = LargeResultsSetPagination
#     queryset = ProductAttributeType.objects.all()
#     serializer_class = ProductAttributeTypeSerializer
#     lookup_field = "uuid"  # Individual object will be found by this field
#     filter_by_query_parm = "name"
#     model = ProductAttributeType

#     def perform_create(self, serializer, request):
#         serializer.save()

#     def perform_update(self, instance, serializer, request):
#         """Update an existing Brand and store activity log."""
#         previous_data_before_update = self.queryset.get(uuid=instance.uuid)
#         serializer.save()

#     def perform_destroy(self, instance, request):
#         serializer = self.serializer_class(instance).data
#         instance.delete()

#     def perform_soft_delete(self, instance, request):
#         instance.is_active = False
#         instance.is_soft_deleted = True
#         instance.save()

#     def list(self, request, *args, **kwargs):
#         if not request.instance.is_staff:
#             # Customer request
#             queryset = self.get_queryset().filter(is_active=True, is_soft_deleted=False)
#         else:
#             # stuff request
#             queryset = self.get_queryset().filter(is_soft_deleted=False)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response({"data": serializer.data}, status=status.HTTP_200_OK)

#     def create(self, request, *args, **kwargs):
#         data = request.data

#         serializer = self.get_serializer(data=data)
#         if not serializer.is_valid():
#             return Response(
#                 {"details": serializer.errors},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         self.perform_create(serializer, request)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def update(self, request, *args, **kwargs):
#         data = request.data
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=data, partial=True)

#         if not serializer.is_valid():
#             return Response(
#                 {"details": serializer.errors},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         self.perform_update(instance, serializer, request)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()  # get the requested object instance

#         # soft delete
#         if request.GET.get("sd", 0):
#             self.perform_soft_delete(instance, request)
#         else:
#             self.perform_destroy(instance, request)
#         return Response(
#             {"detail": "ProductAttributeType deleted successfully"},
#             status=status.HTTP_200_OK,
#         )


# class ProductAttributeViewSet(BaseGenericAPIView):
#     permission_classes = [AuthenticatedStaffOrReadOnly]
#     pagination_class = LargeResultsSetPagination
#     queryset = ProductAttribute.objects.all()
#     model = ProductAttribute
#     serializer_class = ProductAttributeSerializer
#     lookup_field = "uuid"  # Individual object will be found by this field
#     search_keywords = ["type__name"]
#     filter_by_query_parm = "product__uuid"

#     def find_product_by_uuid(self, uuid):
#         try:
#             return Product.objects.get(uuid=uuid)
#         except ObjectDoesNotExist:
#             return None

#     def perform_create(self, serializer, request):
#         serializer.save()

#     def perform_update(self, instance, serializer, request):
#         """Update an existing Brand and store activity log."""
#         previous_data_before_update = self.queryset.get(uuid=instance.uuid)
#         serializer.save()

#     def perform_destroy(self, instance, request):
#         serializer = self.serializer_class(instance).data
#         instance.delete()

#     def perform_soft_delete(self, instance, request):
#         instance.is_active = False
#         instance.is_soft_deleted = True
#         instance.save()
#         serializer = self.serializer_class(instance).data

#     def list(self, request, *args, **kwargs):
#         if not request.instance.is_staff:
#             # Customer request
#             queryset = self.get_queryset().filter(is_active=True, is_soft_deleted=False)
#         else:
#             # stuff request
#             queryset = self.get_queryset().filter(is_soft_deleted=False)

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response({"data": serializer.data}, status=status.HTTP_200_OK)

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         data._mutable = True

#         product = self.find_product_by_uuid(data.get("product"))
#         data["product"] = product.id
#         data._mutable = False

#         serializer = self.get_serializer(data=data)
#         if not serializer.is_valid():
#             return Response(
#                 {"details": serializer.errors},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         self.perform_create(serializer, request)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def update(self, request, *args, **kwargs):
#         data = request.data
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=data, partial=True)

#         if not serializer.is_valid():
#             return Response(
#                 {"details": serializer.errors},
#                 status=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             )

#         self.perform_update(instance, serializer, request)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()  # get the requested object instance

#         # soft delete
#         if request.GET.get("sd", 0):
#             self.perform_soft_delete(instance, request)
#         else:
#             self.perform_destroy(instance, request)
#         return Response(
#             {"detail": "ProductAttribute deleted successfully"},
#             status=status.HTTP_200_OK,
#         )
