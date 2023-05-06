from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.base.custom_pagination import LargeResultsSetPagination
from apps.core.base.custom_viewset import BaseGenericAPIView
from apps.core.base.drf_custom_permisson import AuthenticatedStaffOrReadOnly
from apps.core.base.utils.basic import *
from apps.main.inventory.models import Product
from apps.main.shop.service import ShopOrderProcess

from ...models import Shop, Shopkeeper, ShopOrder, ShopProduct
from .serializers import (
    ShopkeeperSerializer,
    ShopOrderSerializer,
    ShopProductInputSerializer,
    ShopProductSerializer,
    ShopSerializer,
)

User = get_user_model()


class ShopMixin:
    lookup_field = "uuid"  # Individual object will be found by this field

    def perform_create(self, serializer, request, name=""):
        serializer.save()

    def perform_update(self, instance, serializer, request, name=""):
        previous_data_before_update = self.queryset.get(uuid=instance.uuid)
        if not name and hasattr(previous_data_before_update, "name"):
            name = previous_data_before_update.name
        serializer.save()

    def perform_destroy(self, instance, request, name=""):
        serializer = self.serializer_class(instance)
        instance.delete()

    def perform_soft_delete(self, instance, request, name=""):
        instance.is_active = False
        instance.is_soft_deleted = True
        instance.save()
        serializer = self.serializer_class(instance)


class ShopViewSet(ShopMixin, viewsets.ModelViewSet):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    pagination_class = LargeResultsSetPagination
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    search_keywords = ["name", "location"]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_soft_deleted=False)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance

        # soft delete
        if request.GET.get("sd", 0):
            self.perform_soft_delete(instance, request)
        else:
            self.perform_destroy(instance, request)
        return Response(
            {"detail": "Shop deleted successfully"}, status=status.HTTP_200_OK
        )


class ShopkeeperViewSet(ShopMixin, viewsets.ModelViewSet):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    queryset = Shopkeeper.objects.all()
    serializer_class = ShopkeeperSerializer

    def list(self, request, *args, **kwargs):
        shop_uuid = request.GET.get("shop_uuid", None)
        if not shop_uuid:
            return Response(
                {"data": "shop uuid required"}, status=status.HTTP_400_BAD_REQUEST
            )
        queryset = self.get_queryset().filter(
            shop__uuid=shop_uuid, is_soft_deleted=False
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        shop_uuid = request.GET.get("shop_uuid", None)
        if not shop_uuid:
            return Response(
                {"data": "shop uuid required"}, status=status.HTTP_400_BAD_REQUEST
            )
        data = request.data
        shop = Shop.objects.get(uuid=shop_uuid)
        temp_data = []
        for employee in data["employee"]:
            temp_data.append({"employee": employee, "shop": shop.id})
        # add
        for temp in temp_data:
            serializer = self.get_serializer(data=temp)
            if not serializer.is_valid():
                return Response(
                    {"details": serializer.errors},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
            try:
                self.perform_create(serializer, request, name="")
            except IntegrityError:
                # duplicate data
                pass

        # delete
        available_employee = Shopkeeper.objects.filter(
            shop__uuid=shop_uuid
        ).values_list("employee_id", flat=True)
        deletable_employee = list(
            set(available_employee) - set(list(map(int, data["employee"])))
        )
        deletable_shopkeepers = Shopkeeper.objects.filter(
            shop__uuid=shop_uuid, employee_id__in=deletable_employee
        )
        for _ in deletable_shopkeepers:
            self.perform_destroy(_, request, name=_.employee.name)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        self.perform_update(instance, serializer, request, name=instance.employee.name)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance

        # soft delete
        if request.GET.get("sd", 0):
            self.perform_soft_delete(instance, request, name=instance.employee.name)
        else:
            self.perform_destroy(instance, request, name=instance.employee.name)
        return Response(
            {"detail": "Shopkeeper deleted successfully"}, status=status.HTTP_200_OK
        )


class ShopProductViewSet(ShopMixin, BaseGenericAPIView):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    pagination_class = LargeResultsSetPagination
    queryset = ShopProduct.objects.all()
    model = Product
    serializer_class = ShopProductSerializer
    search_keywords = ["product_id"]

    def list(self, request, *args, **kwargs):
        # list of all products with ShopProduct selected
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        shop_uuid = request.GET.get("shop_uuid", None)
        if not shop_uuid:
            return Response(
                {"data": "shop uuid required"}, status=status.HTTP_400_BAD_REQUEST
            )
        data = request.data
        pid = Product.objects.get(uuid=data["product_uuid"]).id
        sid = Shop.objects.get(uuid=shop_uuid).id
        try:
            instance = ShopProduct.objects.get(product_id=pid, shop_id=sid)
        except Exception:
            instance = None

        temp_data = {
            "product": pid,
            "shop": sid,
            "stock": data["stock"],
            "is_active": data["is_active"],
        }
        if instance:
            serializer = ShopProductInputSerializer(instance, data=temp_data)
        else:
            serializer = ShopProductInputSerializer(data=temp_data)

        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        try:
            self.perform_create(serializer, request, name="")
        except IntegrityError:
            # duplicate data
            self.perform_update(
                instance, serializer, request, name=instance.product.product_id
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        self.perform_update(
            instance, serializer, request, name=instance.product.product_id
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance

        # soft delete
        if request.GET.get("sd", 0):
            self.perform_soft_delete(
                instance, request, name=instance.product.product_id
            )
        else:
            self.perform_destroy(instance, request, name=instance.product.product_id)
        return Response(
            {"detail": "ShopProduct deleted successfully"}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["GET"], name="Shop Products")
    def search(self, request, *args, **kwargs):
        shop = None
        query_param = self.request.GET.get("q", "")
        shopkeeper = Shopkeeper.objects.filter(employee=request.user)
        if shopkeeper.exists():
            shop = shopkeeper.first().shop
            queryset = ShopProduct.objects.filter(
                shop=shop,
                product__is_active=True,
                product__manufacturer__is_active=True,
                product__category__is_active=True,
                is_active=True,
            )
        else:
            queryset = ShopProduct.objects.filter(
                product__is_active=True,
                product__manufacturer__is_active=True,
                product__category__is_active=True,
                is_active=True,
            )

        if query_param == "":
            queryset = queryset[:30]
            data = self.generate_shop_product_response(queryset)
            serializer = self.get_serializer(data, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        queryset = queryset.filter(product__product_id=query_param)
        data = self.generate_shop_product_response(queryset)
        serializer = self.get_serializer(data, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def generate_shop_product_response(self, shop_products: ShopProduct) -> dict:
        data = []
        for shop_product in shop_products:
            shop_product.product.stock = shop_product.stock
            data.append(shop_product.product)
        return data


class ShopOrderPOSViewSet(ShopMixin, BaseGenericAPIView):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    pagination_class = LargeResultsSetPagination
    queryset = ShopOrder.objects.all()
    model = ShopOrder
    serializer_class = ShopOrderSerializer
    service_class = ShopOrderProcess

    def list(self, request, *args, **kwargs):
        service = self.service_class(request_user_id=request.user.id)
        active_order = service.active_order_of_shopkeeper()
        if active_order:
            active_order.order_lines = service.get_orderlines()
            active_order.extra_lines = service.get_extralines()
            serializer = self.get_serializer([active_order], many=True)
        else:
            serializer = self.get_serializer([], many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        shopkeeper = Shopkeeper.objects.filter(employee=request.user)
        if not shopkeeper.exists():
            return Response(
                {"details": "You are not an authorized shopkeeper"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        service = self.service_class(request_user_id=request.user.id)
        order = service.add_lines(**request.data)
        if order:
            order.order_lines = service.get_orderlines()
            order.extra_lines = service.get_extralines()
        serializer = self.serializer_class(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        shopkeeper = Shopkeeper.objects.filter(employee=request.user)
        if not shopkeeper.exists():
            return Response(
                {"details": "You are not an authorized shopkeeper"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        service = self.service_class(request_user_id=request.user.id)
        order = service.delete_lines(**request.data)
        if order:
            order.order_lines = service.get_orderlines()
            order.extra_lines = service.get_extralines()
        serializer = self.serializer_class(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], name="Confirm order")
    def complete_order(self, request, *args, **kwargs):
        shopkeeper = Shopkeeper.objects.filter(employee=request.user)
        if not shopkeeper.exists():
            return Response(
                {"details": "You are not an authorized shopkeeper"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        service = self.service_class(request_user_id=request.user.id)
        order = service.complete_order()
        if order:
            order.order_lines = service.get_orderlines()
            order.extra_lines = service.get_extralines()
        else:
            return Response(
                {"details": "Failed!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.serializer_class(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], name="Delete order")
    def delete_order(self, request, *args, **kwargs):
        shopkeeper = Shopkeeper.objects.filter(employee=request.user)
        if not shopkeeper.exists():
            return Response(
                {"details": "You are not an authorized shopkeeper"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        service = self.service_class(request_user_id=request.user.id)
        order = service.delete_order()
        if order == 400:
            return Response(
                {"details": "Can't delete order as it is already confirmed!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif order != 200:
            return Response(
                {"details": "Failed!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"details": "Success!"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], name="Search order")
    def search(self, request, *args, **kwargs):
        service = self.service_class(request_user_id=request.user.id)
        order_code = request.GET["code"]
        if not order_code.startswith("H0000"):
            return Response(
                {"details": "Invalid Code!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order_id = order_code.replace("H0000", "")
        order = service.get_order(id=order_id)
        if order:
            order.order_lines = service.get_orderlines()
            order.extra_lines = service.get_extralines()
            order.shop = service.get_shop()
            serializer = self.get_serializer([order], many=True)
        else:
            serializer = self.get_serializer([], many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class ShopOrderViewSet(ShopMixin, BaseGenericAPIView):
    permission_classes = [AuthenticatedStaffOrReadOnly]
    pagination_class = LargeResultsSetPagination
    queryset = ShopOrder.objects.all()
    model = ShopOrder
    serializer_class = ShopOrderSerializer
    lookup_field = "uuid"  # Individual object will be found by this field
    service_class = ShopOrderProcess

    def list(self, request, *args, **kwargs):
        shop_uuid = request.GET.get("shop_uuid", None)
        if not shop_uuid:
            return Response(
                {"data": "shop uuid required"}, status=status.HTTP_400_BAD_REQUEST
            )
        orders = (
            self.model.objects.filter(shop__uuid=shop_uuid)
            .select_related("shop")
            .order_by("-updated_at")
        )
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_object()
        service = self.service_class(request_user_id=request.user.id, order=queryset)
        queryset.discount = fix_external_decimal_places(queryset.discount)
        queryset.tax = fix_external_decimal_places(queryset.tax)
        queryset.order_lines = service.get_orderlines()
        queryset.extra_lines = service.get_extralines()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
