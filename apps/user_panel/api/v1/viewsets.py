import datetime
import json
import os
import logging
import operator
from functools import reduce

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.db import transaction
from django.db.models import Q
from django.template.loader import render_to_string

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from weasyprint import HTML

from apps.base.utils.basic import *
from apps.rbac.api.v1.serializers import UserInputSerializer
from apps.send_email.api.v1.viewsets import new_order_notify_email_to_owner
from apps.base.drf_custom_permisson import AuthenticatedStaffOrReadOnly
from apps.base.custom_viewset import BaseGenericAPIView
from apps.base.custom_pagination import LargeResultsSetPagination
from apps.finale_inventory.api.v1.viewsets import Finaleinventory.
from apps.inventory.api.v1.serializers import ProductSerializer
from apps.inventory.api.v1.viewsets import is_authorized_dealer
from apps.inventory.models import Product, DealerBrand, StockTransaction
from apps.user_panel.models import (
    Cart,
    Expense,
    ExpenseType,
    InvoiceOrder,
    ManufacturerInvoice,
    Order,
    PurchaseOrder,
    SalesOrder,
    SalesReps,
    DealerSalesReps, FinaleInvoice)
from apps.user_panel.api.v1.serializers import (
    CartSerializer,
    ExpenseSerializer,
    ExpenseTypeSerializer,
    InvoiceOrderSerializer,
    ManufacturerInvoiceSerializer,
    OrderSerializer,
    PurchaseOrderSerializer,
    SalesOrderSerializer,
    SalesRepsSerializer,
    FinaleInvoiceSerializer)
from apps.user_panel.online_payment import OnlinePayment

User = get_user_model()


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'uuid'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        serializer.save()

    def perform_update(self, instance, serializer, request):
        """ Update an existing Cart and store activity log. """
        serializer.save()

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        instance.delete()

    def perform_soft_delete(self, instance, request):
        instance.is_active = False
        instance.is_soft_deleted = True
        instance.save()
        serializer = self.serializer_class(instance).data

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            # Customer request
            queryset = self.get_queryset().filter(
                user=request.user,
                is_ordered=False,
                is_active=True,
                is_soft_deleted=False
            )
        else:
            # stuff request
            queryset = self.get_queryset().filter(is_soft_deleted=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        product = Product.objects.get(uuid=data['product'])

        is_product_already_in_cart = Cart.objects.filter(
            user=request.user,
            product=product,
            is_ordered=False
        ).exists()

        # check dealer authorization status for authorization required products
        if is_authorized_dealer(product.manufacturer, request.user) is False:
            return Response({
                'detail': f'Please request for authorization'
            }, status=status.HTTP_400_BAD_REQUEST)

        # check manual product
        # if this is a manual product and stock 0 then show phone number to order
        if not product.added_from_finale and product.stock in [None, '', 0]:
            return Response({'detail': f'Call: {settings.COMPANY_PHONE}'}, status=status.HTTP_400_BAD_REQUEST)

        if not is_product_already_in_cart:
            # create a new cart item for product

            # check quantity available in stock or not
            is_quantity_available = self.check_product_availability(product, int(data['quantity']))
            if not is_quantity_available:
                return Response({'detail': 'Quantity unavailable'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                discount = float(DealerBrand.objects.get(
                    dealer=request.user,
                    brand=product.manufacturer
                ).discount)
            except Exception as ex:
                discount = 0
            try:
                data['user'] = request.user.id
                data['product'] = product.id
                data['product_json'] = ProductSerializer(product).data
                data['unit_price'] = product.your_price
                data['total_price'] = round((
                    (float(product.your_price) * int(data['quantity'])) -
                    (
                        (
                                (float(product.your_price) * int(data['quantity'])) * discount
                        ) / 100
                    )
                ), 2)
                data['discount'] = discount
            except Exception as ex:
                logging.getLogger('warning_logger').warning(ex.__str__())

            serializer = self.get_serializer(data=data)
            if not serializer.is_valid():
                return Response({"details": serializer.errors},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            self.perform_create(serializer, request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # update an existing cart item for product
            instance = Cart.objects.filter(
                user=request.user,
                product=product,
                is_ordered=False
            )[0]

            try:
                data['product'] = instance.product.id
                data['quantity'] = int(instance.quantity) + int(data['quantity'])

                # check quantity available in stock or not
                is_quantity_available = self.check_product_availability(product, int(data['quantity']))
                if not is_quantity_available:
                    return Response({'detail': 'Quantity unavailable'}, status=status.HTTP_400_BAD_REQUEST)

                data['total_price'] = round((
                    (float(instance.product.your_price) * data['quantity']) -
                    (
                        (
                            (float(instance.product.your_price) * data['quantity']) * float(instance.discount)
                        ) / 100
                    )
                ), 2)
            except Exception as ex:
                logging.getLogger('warning_logger').warning(ex.__str__())

            serializer = self.get_serializer(instance, data=data, partial=True)
            if not serializer.is_valid():
                return Response({"details": serializer.errors},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            self.perform_update(instance, serializer, request)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data

        instance = self.get_object()

        if instance.is_ordered:
            return Response('Cart item already ordered', status=status.HTTP_400_BAD_REQUEST)

        # check quantity available in stock or not
        is_quantity_available = self.check_product_availability(instance.product, int(data['quantity']))
        if not is_quantity_available:
            return Response({'detail': 'Quantity unavailable'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data['total_price'] = round((
                (float(instance.product.your_price) * float(data['quantity'])) -
                (
                    (
                        (float(instance.product.your_price) * float(data['quantity'])) * float(instance.discount)
                    ) / 100
                )
            ), 2)
        except Exception as ex:
            logging.getLogger('warning_logger').warning(ex.__str__())

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance

        # soft delete
        if request.GET.get('sd', 0):
            self.perform_soft_delete(instance, request)
        else:
            self.perform_destroy(instance, request)
        return Response({"detail": "Cart item deleted successfully"},
                        status=status.HTTP_200_OK)

    def check_product_availability(self, product, quantity):
        product_id = product.product_id

        if product_id is None:
            return Response({"details": "Product ID required"}, status=status.HTTP_400_BAD_REQUEST)

        if not product.added_from_finale:
            if int(product.stock) > quantity:
                return True
            else:
                return False
        else:
            try:
                # authenticate to finale
                finale_inventory= Finaleinventory.(
                    settings.FINALE_URL,
                    settings.FINALE_USERNAME,
                    settings.FINALE_PASSWORD,
                )
                # request for product
                response = finale_inventory.get_product_details(
                    {
                        "operationName": None,
                        "variables": {},
                        "query": "query Rows($after: String, $first: Int) { "
                                 "productViewConnection(status: [\"PRODUCT_ACTIVE\"], "
                                 f"search: \"{product_id}\", "
                                 "after: $after, first: $first, sort: [{field: \"productId\", "
                                 "mode: \"asc\"}]) { edges { node(timezone: \"Asia/Dhaka\")"
                                 " { "
                                 "unitsInStock "
                                 "}}}}"
                    }
                )

                if response['status']:
                    # successful response
                    available_stock = int(response['data'][0]['node']['unitsInStock'])
                    if available_stock >= quantity:
                        return True
                    else:
                        return False
                else:
                    return False
            except Exception as ex:
                logging.getLogger('warning_logger').warning(ex.__str__())
                return False


class PaymentFailed(Exception):
    pass


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'uuid'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        serializer.save()

    def perform_update(self, instance, serializer, request):
        """ Update an existing Order and store activity log. """
        serializer.save()

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        instance.delete()

    def perform_soft_delete(self, instance, request):
        instance.is_active = False
        instance.is_soft_deleted = True
        instance.save()
        serializer = self.serializer_class(instance).data

    def list(self, request, *args, **kwargs):
        show_cancellations = int(request.GET.get('cancellation', 0))
        show_processing = int(request.GET.get('processing', 0))
        show_delivered = int(request.GET.get('delivered', 0))
        show_pending = int(request.GET.get('pending', 0))

        if not request.user.is_staff:
            # Customer request
            queryset = self.get_queryset().filter(
                user=request.user,
                is_ordered=True,
                is_cancelled=show_cancellations,
                is_active=True,
                is_soft_deleted=False
            )
        else:
            # stuff request
            queryset = self.get_queryset().filter(is_soft_deleted=False)

            if show_pending:
                queryset = queryset.filter(
                    is_ordered=True,
                    in_processing=False,
                    is_delivered=False,
                    is_cancelled=False
                )

            if show_processing:
                queryset = queryset.filter(
                    in_processing=True,
                    is_delivered=False,
                    is_cancelled=False
                )

            if show_delivered:
                queryset = queryset.filter(
                    in_processing=True,
                    is_delivered=True,
                    is_cancelled=False
                )

            if show_cancellations:
                queryset = queryset.filter(
                    is_cancelled=True
                )

        queryset = queryset.order_by('-id')

        if request.GET.get('draw'):
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        carts = Cart.objects.filter(
            user=request.user,
            is_ordered=False,
            is_active=True,
            is_soft_deleted=False
        )
        carts_json = CartSerializer(carts, many=True).data
        # calculate total price sum([20.00, 40.00]) = 60.00
        total_price = sum(
            [float(price) for price in carts.values_list(
                'total_price', flat=True
            )]
        )
        try:
            data['user'] = request.user.id
            data['user_details'] = UserInputSerializer(request.user).data
            data['carts'] = [cart.id for cart in carts]
            data['carts_json'] = carts_json
            data['total_price'] = total_price
            data['is_ordered'] = True
            data['po_number'] = data['billing_info']['po_number']
            data['billing_full_name'] = data['billing_info']['full_name']
            data['billing_address'] = data['billing_info']['billing_address']
            data['billing_city'] = data['billing_info']['city']
            data['billing_state'] = json.dumps(data['billing_info']['state'])
            data['billing_postal_code'] = data['billing_info']['postal_code']
            data['billing_phone'] = data['billing_info']['phone']
            data['billing_email'] = data['billing_info']['email']
            data['shipping_full_name'] = data['shipping_info']['full_name']
            data['delivery_address'] = data['shipping_info']['delivery_address']
            data['shipping_city'] = data['shipping_info']['city']
            data['shipping_state'] = json.dumps(data['shipping_info']['state'])
            data['shipping_postal_code'] = data['shipping_info']['postal_code']
            data['shipping_phone'] = data['shipping_info']['phone']
            data['shipping_email'] = data['shipping_info']['email']
            data['transaction_code'] = 'PENDING_PAYMENT'
            data['transaction_response'] = {'status': 'PENDING_PAYMENT'}
        except Exception as ex:
            logging.getLogger('warning_logger').warning(ex.__str__())

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        invoice_path = ''
        try:
            with transaction.atomic():
                self.perform_create(serializer, request)

                # update cart items
                carts.update(is_ordered=True)

                # create folder if not exists
                if not default_storage.exists(settings.ORDER_INVOICE):
                    os.makedirs(default_storage.path(settings.ORDER_INVOICE))

                # generate invoice
                order = Order.objects.get(id=serializer.data['id'])
                html_string = render_to_string(
                    'send_email/order/invoice.html',
                    {
                        'data': order,
                        'billing_state': data['billing_info']['state']['text'],
                        'shipping_state': data['shipping_info']['state']['text'],
                    }
                )
                html = HTML(string=html_string, base_url=request.build_absolute_uri())
                path = f'{default_storage.path(settings.ORDER_INVOICE)}/invoice_{random_hex_code(16)}.pdf'
                html.write_pdf(target=path)
                order.invoice = path.replace(default_storage.path('') + '/', '')
                invoice_path = order.invoice
                order.save()

                logging.getLogger('success_logger').info(
                    {f'SUCCESSFUL_ORDER_CREATED - 140{order.id}': serializer.data}
                )
                logging.getLogger('success_logger').info(
                    f'=============>> STARTING PAYMENT PROCESS - 140{order.id}'
                )

                # process Authorized.net payment
                data['id'] = str(order.id)
                payment = OnlinePayment().create_an_accept_payment_transaction(
                    data=data
                )

                if payment['status'] == 400:
                    raise PaymentFailed(payment["details"])

                if payment['status'] == 200:
                    # save transaction info
                    order.transaction_code = payment['data']['transactionResponse']['transId']
                    order.transaction_response = payment['data']
                    order.save()
                    # Inform owner about new order
                    new_order_notify_email_to_owner(request, order)
                    return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            # delete invoice
            default_storage.delete(invoice_path)
            logging.getLogger('warning_logger').warning(ex.__str__())
            return Response({'details': ex.__str__()}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        invoice_path = f'{default_storage.path(settings.ORDER_INVOICE)}/invoice_{random_hex_code(16)}.pdf'

        # only cancellation is allowed
        for key in ['user', 'carts', 'carts_json', 'total_price', 'is_ordered']:
            if data.get(key):
                del data[key]

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            # void a transaction at payment gateway
            void_transaction = OnlinePayment().void_transaction(
                refTransId=instance.transaction_code
            )

            if void_transaction['status'] == 400:
                raise PaymentFailed(void_transaction["details"])

            if void_transaction['status'] == 200:
                self.perform_update(instance, serializer, request)

                order = instance
                # remove existing/previous invoice
                default_storage.delete(order.invoice)

                # generate new invoice
                html_string = render_to_string(
                    'send_email/order/invoice.html',
                    {'data': order}
                )
                html = HTML(string=html_string, base_url=request.build_absolute_uri())
                html.write_pdf(target=invoice_path)
                order.invoice = invoice_path.replace(default_storage.path('') + '/', '')
                order.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            # delete invoice
            if default_storage.exists(invoice_path):
                default_storage.delete(invoice_path)
            logging.getLogger('warning_logger').warning(ex.__str__())
            return Response({'details': ex.__str__()}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance

        # soft delete
        # if request.GET.get('sd', 0):
        #     self.perform_soft_delete(instance, request)
        # else:
        #     self.perform_destroy(instance, request)
        return Response({"detail": "Order item deleted not allowed"},
                        status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, name="Already used address in an order")
    def get_user_used_address(self, request, *args, **kwargs):
        user = request.user
        is_shipping_address = int(request.GET.get('shipping', 0))
        text = request.GET.get('text')
        data = []

        if is_shipping_address:
            orders = Order.objects.filter(
                user=user,
            ).distinct(
                'shipping_full_name',
                'delivery_address',
                'shipping_city',
                'shipping_state',
                'shipping_postal_code',
                'shipping_phone',
                'shipping_email'
            )

            for order in orders:
                data.append({
                    'full_name':order.shipping_full_name,
                    'address':order.delivery_address,
                    'city':order.shipping_city,
                    'state':order.shipping_state,
                    'postal_code':order.shipping_postal_code,
                    'phone':order.shipping_phone,
                    'email':order.shipping_email
                })
        else:
            orders = Order.objects.filter(
                user=user,
            ).distinct(
                'billing_full_name',
                'billing_address',
                'billing_city',
                'billing_state',
                'billing_postal_code',
                'billing_phone',
                'billing_email'
            )

            for order in orders:
                data.append({
                    'full_name':order.billing_full_name,
                    'address':order.billing_address,
                    'city':order.billing_city,
                    'state':order.billing_state,
                    'postal_code':order.billing_postal_code,
                    'phone':order.billing_phone,
                    'email':order.billing_email
                })

        return Response({"data": data}, status=status.HTTP_200_OK)


class SalesRepsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    queryset = SalesReps.objects.all()
    serializer_class = SalesRepsSerializer
    lookup_field = 'uuid'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        serializer.save()

    def perform_update(self, instance, serializer, request):
        """ Update an existing SalesReps and store activity log. """
        serializer.save()

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        instance.delete()

    def perform_soft_delete(self, instance, request):
        instance.is_active = False
        instance.is_soft_deleted = True
        instance.save()
        serializer = self.serializer_class(instance).data

    def list(self, request, *args, **kwargs):

        if not request.user.is_staff:
            # Customer request
            queryset = self.get_queryset().filter(
            )
        else:
            # stuff request
            queryset = self.get_queryset().filter(is_soft_deleted=False)

        queryset = queryset.order_by('-id')
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        # store files in server
        for file in files:
            file_path = f'{settings.SALES_REPS_IMAGE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        # store files in server
        for file in files:
            file_path = f'{settings.SALES_REPS_IMAGE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance

        # soft delete
        if request.GET.get('sd', 0):
            self.perform_soft_delete(instance, request)
        else:
            self.perform_destroy(instance, request)
        return Response({"detail": "SalesReps item deleted not allowed"},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], name='Set Sales Resp at User Edit Dropdown')
    def sales_reps_dropdown_value(self, request, *args, **kwargs):
        user_uuid = request.GET.get('user')
        response_data = []
        selected_sales_reps = []
        sales_reps = self.queryset
        requested_users_sales_reps = DealerSalesReps.objects.filter(
            dealer__uuid=user_uuid
        )

        if requested_users_sales_reps.exists():
            selected_sales_reps = list(
                requested_users_sales_reps[0].sales_reps.all().values_list(
                    'id', flat=True
                )
            )

        for rep in sales_reps:
            selected = False
            if rep.id in selected_sales_reps:
                selected = True
            response_data.append(
                {
                    'id': rep.uuid,
                    'name': rep.name,
                    'title': rep.title,
                    'image': rep.image,
                    'phone': rep.phone,
                    'email': rep.email,
                    'selected': selected,
                    'text': f"{rep.name} ({rep.title})",
                }
            )
        return Response({"detail": response_data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], name='Set Sales Resp at User Edit Dropdown')
    def sales_reps_add_update(self, request, *args, **kwargs):
        data = request.data
        user_uuid = request.GET.get('user')
        dealer = User.objects.get(uuid=user_uuid)
        sales_reps = DealerSalesReps.objects.filter(
            dealer__uuid=user_uuid
        )
        requested_sr = SalesReps.objects.filter(uuid__in=data['sales_reps'])

        if sales_reps.exists():
            sr = sales_reps[0]
            sr.sales_reps.clear()
        else:
            sr = DealerSalesReps()
            sr.dealer = dealer
        sr.save()

        for i in requested_sr:
            sr.sales_reps.add(i)

        return Response({"detail": 'done'}, status=status.HTTP_200_OK)


class FinaleInvoiceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    queryset = FinaleInvoice.objects.all()
    serializer_class = FinaleInvoiceSerializer
    lookup_field = 'uuid'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        serializer.save()

    def perform_update(self, instance, serializer, request):
        """ Update an existing FinaleInvoice and store activity log. """
        serializer.save()

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        instance.delete()

    def perform_soft_delete(self, instance, request):
        instance.is_active = False
        instance.is_soft_deleted = True
        instance.save()
        serializer = self.serializer_class(instance).data

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            # Customer request
            queryset = self.get_queryset().filter(
                dealer=self.request.user
            )
        else:
            # stuff request
            user_uuid = self.request.GET.get('uuid', None)
            queryset = self.get_queryset().filter(
                dealer=User.objects.get(uuid=user_uuid),
                is_soft_deleted=False
            )

        queryset = queryset.order_by('-id')
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        data._mutable = True
        # store files in server
        for file in files:
            file_path = f'{settings.FINALE_INVOICE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path

        data['dealer'] = User.objects.get(uuid=data['dealer']).id

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        # store files in server
        for file in files:
            file_path = f'{settings.SALES_REPS_IMAGE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance

        # soft delete
        if request.GET.get('sd', 0):
            self.perform_soft_delete(instance, request)
        else:
            self.perform_destroy(instance, request)
        return Response({"detail": "FinaleInvoice item deleted"},
                        status=status.HTTP_200_OK)


class SalesOrderViewSet(BaseGenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    model = SalesOrder
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    lookup_field = 'uuid'  # Individual object will be found by this field
    search_keywords = ["number", "date", "due_date", "notes", "created_at"]

    def perform_create(self, serializer, request):
        serializer.save()

    def perform_update(self, instance, serializer, request):
        """ Update an existing SalesOrder and store activity log. """
        serializer.save()

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        instance.delete()

    def perform_soft_delete(self, instance, request):
        instance.is_active = False
        instance.is_soft_deleted = True
        instance.save()
        serializer = self.serializer_class(instance).data

    @staticmethod
    def string_to_datetime_object(str_date):
        return datetime.datetime.strptime(str_date, '%m/%d/%Y')

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            # Customer request
            queryset = self.get_queryset().filter(
                dealer=self.request.user
            )
        else:
            # stuff request
            queryset = self.get_queryset().filter(
                is_soft_deleted=False
            )
        if request.GET.get("term"):
            queryset = queryset.filter(number__icontains=request.GET.get("term"))
        
        if request.GET.get("is_ready_for_processing"):
            queryset = queryset.filter(is_ready_for_processing=True)
        
        if request.GET.get("is_locked"):
            queryset = queryset.filter(is_locked=int(request.GET.get("is_locked")))
        
        if request.GET.get("is_paid"):
            filtered = (x.id for x in queryset if x.is_paid==int(request.GET.get("is_paid")))
            queryset = queryset.filter(id__in=filtered)

        # date range filter
        if request.GET.get("date_range") not in ["", None]:
            _from, _to = request.GET.get("date_range").split(" - ")
            queryset = queryset.filter(
                created_at__range=[
                    self.string_to_datetime_object(_from),
                    self.string_to_datetime_object(_to) + datetime.timedelta(days=1)
                ]
            )

        if not queryset.exists() and request.GET.get("search[value]"):
            query = [Q(**{f"data__products__{i}__product_id__icontains": self.request.GET.get('search[value]', None)}) for i in range(50)]
            queryset = self.model.objects.filter(reduce(operator.or_, query))
            
        queryset = queryset.order_by('-id')
        if request.GET.get('draw'):
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True, context={'empty_data': True})
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context={'empty_data': True})
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()

        if data.get("is_locked", True) and instance.is_locked:
            return Response({
                "details": [
                    {0: 'SO already updated and locked. No more modification allowed.'}
                ]
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # if data.get('is_stock_updated', False):
        #     is_stock_updated = self.update_stock(instance.data['products']) 
        #     if is_stock_updated['status'] == 'failed':
        #         return Response({
        #             "details": is_stock_updated['details']
        #         }, status=status.HTTP_406_NOT_ACCEPTABLE)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance

        if instance.is_locked:
            return Response({
                "details": [
                    {0: 'SO already updated and locked. Deletion not allowed.'}
                ]
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        # soft delete
        if request.GET.get('sd', 0):
            self.perform_soft_delete(instance, request)
        else:
            self.perform_destroy(instance, request)
        return Response({"detail": "SalesOrder deleted"},
                        status=status.HTTP_200_OK)

    def update_stock(self, products: list) -> dict:
        status = 'success'
        details = []
        failed = False

        product_ids = [int(product['id']) for product in products]
        queue = []

        # check all products are available
        if (
            len(product_ids) != Product.objects.filter(id__in=product_ids).count()
        ):
            failed = True
            status = 'failed'
            details.append({0: "One of the product doesn't exist"})

        if not failed:
            for product in products:
                try:
                    p = Product.objects.get(id=product["id"])

                    current_stock = ''
                    if p.stock in [None, '']:
                        current_stock = '0'
                    else:
                        current_stock = p.stock

                    new_stock = int(current_stock) - int(product['quantity'])
                    if new_stock < 0:
                        new_stock = 0
                    p.stock = new_stock
                    queue.append(p)
                except Exception as ex:
                    failed = True
                    status = 'failed'
                    details.append({0: ex.__stt__()})
                    break

        if not failed:
            for q in queue:
                q.save()

        return {
            'status': status,
            'details': details
        }


class PurchaseOrderViewSet(BaseGenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    model = PurchaseOrder
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'uuid'  # Individual object will be found by this field
    search_keywords = ["number", "date", "due_date", "notes", "created_at"]

    def perform_create(self, serializer, request):
        serializer.save()

    def perform_update(self, instance, serializer, request):
        """ Update an existing PurchaseOrder and store activity log. """
        serializer.save()

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        instance.delete()

    def perform_soft_delete(self, instance, request):
        instance.is_active = False
        instance.is_soft_deleted = True
        instance.save()
        serializer = self.serializer_class(instance).data

    @staticmethod
    def string_to_datetime_object(str_date):
        return datetime.datetime.strptime(str_date, '%m/%d/%Y')

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            # Customer request
            queryset = self.get_queryset().filter(
                dealer=self.request.user
            )
        else:
            # stuff request
            queryset = self.get_queryset().filter(
                is_soft_deleted=False
            ).values('uuid', 'number', 'date', 'due_date', 'is_stock_updated', 'is_locked', "notes", "created_at")

        if request.GET.get("term"):
            queryset = queryset.filter(number__icontains=request.GET.get("term"))

        if request.GET.get("is_ready_for_processing"):
            queryset = queryset.filter(is_ready_for_processing=True)
        
        if request.GET.get("is_locked"):
            queryset = queryset.filter(is_locked=int(request.GET.get("is_locked")))

        # date range filter
        if request.GET.get("date_range") not in ["", None]:
            _from, _to = request.GET.get("date_range").split(" - ")
            queryset = queryset.filter(
                created_at__range=[
                    self.string_to_datetime_object(_from),
                    self.string_to_datetime_object(_to) + datetime.timedelta(days=1)
                ]
            )
        
        if not queryset.exists() and request.GET.get("search[value]"):
            query = [Q(**{f"data__products__{i}__product_id__icontains": self.request.GET.get('search[value]', None)}) for i in range(50)]
            queryset = self.model.objects.filter(reduce(operator.or_, query))

        queryset = queryset.order_by('-id')        
        if request.GET.get('draw'):
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()

        if data.get("is_locked", True) and instance.is_locked:
            return Response({
                "details": [
                    {0: 'PO already updated and locked. No more modification allowed.'}
                ]
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # if data.get('is_stock_updated', False):
        #     is_stock_updated = self.update_stock(instance.data['products']) 
        #     if is_stock_updated['status'] == 'failed':
        #         return Response({
        #             "details": is_stock_updated['details']
        #         }, status=status.HTTP_406_NOT_ACCEPTABLE)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance

        if instance.is_locked:
            return Response({
                "details": [
                    {0: 'PO already updated and locked. Deletion not allowed.'}
                ]
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        # soft delete
        if request.GET.get('sd', 0):
            self.perform_soft_delete(instance, request)
        else:
            self.perform_destroy(instance, request)
        return Response({"detail": "PurchaseOrder deleted"},
                        status=status.HTTP_200_OK)

    def update_stock(self, products: list) -> dict:
        status = 'success'
        details = []
        failed = False

        product_ids = [int(product['id']) for product in products]
        queue = []

        # check all products are available
        if (
            len(product_ids) != Product.objects.filter(id__in=product_ids).count()
        ):
            failed = True
            status = 'failed'
            details.append({0: "One of the product doesn't exist"})

        if not failed:
            for product in products:
                try:
                    p = Product.objects.get(id=product["id"])

                    current_stock = ''
                    if p.stock in [None, '']:
                        current_stock = '0'
                    else:
                        current_stock = p.stock

                    new_stock = int(current_stock) + int(product['quantity'])
                    p.stock = new_stock
                    queue.append(p)
                except Exception as ex:
                    failed = True
                    status = 'failed'
                    details.append({0: ex.__stt__()})
                    break

        if not failed:
            for q in queue:
                q.save()

        return {
            'status': status,
            'details': details
        }


class ManufacturerInvoiceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    queryset = ManufacturerInvoice.objects.all()
    serializer_class = ManufacturerInvoiceSerializer
    lookup_field = 'uuid'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        serializer.save()

    def perform_update(self, instance, serializer, request):
        """ Update an existing ManufacturerInvoice and store activity log. """
        serializer.save()

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        instance.delete()

    def perform_soft_delete(self, instance, request):
        instance.is_active = False
        instance.is_soft_deleted = True
        instance.save()
        serializer = self.serializer_class(instance).data

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            # Customer request
            pass
        else:
            # stuff request
            queryset = self.get_queryset().filter(
                is_soft_deleted=False
            )

        queryset = queryset.order_by('-id')
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        data._mutable = True
        # store files in server
        for file in files:
            file_path = f'{settings.MANUFACTURER_INVOICE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path
            
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        files = request.FILES

        # store files in server
        for file in files:
            file_path = f'{settings.MANUFACTURER_INVOICE_LOCATION}{files[file].name}'
            path = default_storage.save(file_path, files[file])
            data[file] = path

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance

        # soft delete
        if request.GET.get('sd', 0):
            self.perform_soft_delete(instance, request)
        else:
            self.perform_destroy(instance, request)
        return Response({"detail": "ManufacturerInvoice item deleted"},
                        status=status.HTTP_200_OK)



class InvoiceOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    queryset = InvoiceOrder.objects.all()
    serializer_class = InvoiceOrderSerializer
    lookup_field = 'uuid'  # Individual object will be found by this field

    def perform_create(self, serializer, request):
        serializer.save()

    def perform_update(self, instance, serializer, request):
        """ Update an existing InvoiceOrder and store activity log. """
        serializer.save()

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        instance.delete()

    def perform_soft_delete(self, instance, request):
        instance.is_active = False
        instance.is_soft_deleted = True
        instance.save()
        serializer = self.serializer_class(instance).data

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            # Customer request
            queryset = self.get_queryset().filter(
                dealer=self.request.user
            )
        else:
            # stuff request
            queryset = self.get_queryset().filter(
                is_soft_deleted=False
            )

        queryset = queryset.order_by('-id')
        if request.GET.get('draw'):
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()

        if instance.is_locked:
            return Response({
                "details": [
                    {0: 'Invoice already updated and locked. No more modification allowed.'}
                ]
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # if data.get('is_stock_updated', False):
        #     is_stock_updated = self.update_stock(instance.data['products']) 
        #     if is_stock_updated['status'] == 'failed':
        #         return Response({
        #             "details": is_stock_updated['details']
        #         }, status=status.HTTP_406_NOT_ACCEPTABLE)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance

        if instance.is_locked:
            return Response({
                "details": [
                    {0: 'Invoice already updated and locked. Deletion not allowed.'}
                ]
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        # soft delete
        if request.GET.get('sd', 0):
            self.perform_soft_delete(instance, request)
        else:
            self.perform_destroy(instance, request)
        return Response({"detail": "InvoiceOrder deleted"},
                        status=status.HTTP_200_OK)

    def update_stock(self, products: list) -> dict:
        status = 'success'
        details = []
        failed = False

        product_ids = [int(product['id']) for product in products]
        queue = []

        # check all products are available
        if (
            len(product_ids) != Product.objects.filter(id__in=product_ids).count()
        ):
            failed = True
            status = 'failed'
            details.append({0: "One of the product doesn't exist"})

        if not failed:
            for product in products:
                try:
                    p = Product.objects.get(id=product["id"])

                    current_stock = ''
                    if p.stock in [None, '']:
                        current_stock = '0'
                    else:
                        current_stock = p.stock

                    new_stock = int(current_stock) + int(product['quantity'])
                    p.stock = new_stock
                    queue.append(p)
                except Exception as ex:
                    failed = True
                    status = 'failed'
                    details.append({0: ex.__stt__()})
                    break

        if not failed:
            for q in queue:
                q.save()

        return {
            'status': status,
            'details': details
        }


class ExpenseTypeViewSet(BaseGenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    model = ExpenseType
    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer
    lookup_field = 'uuid'  # Individual object will be found by this field
    search_keywords = ["name", "created_at"]

    def perform_create(self, serializer, request):
        serializer.save()

    def perform_update(self, instance, serializer, request):
        """ Update an existing ExpenseType and store activity log. """
        serializer.save()

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        instance.delete()

    def perform_soft_delete(self, instance, request):
        instance.is_active = False
        instance.is_soft_deleted = True
        instance.save()
        serializer = self.serializer_class(instance).data

    def list(self, request, *args, **kwargs):
        # stuff request
        queryset = self.get_queryset().filter(
            is_soft_deleted=False
        )

        if request.GET.get('draw'):
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True, context={'empty_data': True})
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context={'empty_data': True})
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance

        # soft delete
        if request.GET.get('sd', 0):
            self.perform_soft_delete(instance, request)
        else:
            self.perform_destroy(instance, request)
        return Response({"detail": "ExpenseType deleted"},
                        status=status.HTTP_200_OK)

class ExpenseViewSet(BaseGenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    model = Expense
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    lookup_field = 'uuid'  # Individual object will be found by this field
    search_keywords = ['description', 'type', 'spender', 'created_at', 'created_by']

    def perform_create(self, serializer, request):
        serializer.save()

    def perform_update(self, instance, serializer, request):
        """ Update an existing Expense and store activity log. """
        serializer.save()

    def perform_destroy(self, instance, request):
        serializer = self.serializer_class(instance).data
        instance.delete()

    def perform_soft_delete(self, instance, request):
        instance.is_active = False
        instance.is_soft_deleted = True
        instance.save()
        serializer = self.serializer_class(instance).data

    def list(self, request, *args, **kwargs):
        # stuff request
        queryset = self.get_queryset().filter(
            is_soft_deleted=False
        )

        if request.GET.get('draw'):
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        self.perform_create(serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=data, partial=True)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.perform_update(instance, serializer, request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # get the requested object instance

        # soft delete
        if request.GET.get('sd', 0):
            self.perform_soft_delete(instance, request)
        else:
            self.perform_destroy(instance, request)
        return Response({"detail": "Expense deleted"},
                        status=status.HTTP_200_OK)
