from django.urls import include, path

from .views import *

app_name = "admin_order"

urlpatterns = [
    path(
        "order/",
        include(
            [
                path("", order_list, name="order_list"),
                path("edit/<str:uuid>/", order_edit, name="order_edit"),
            ]
        ),
    ),
    # path('finale-invoice/', include([
    #     path('', finale_invoice_list, name='finale_invoice_list'),
    #     path('edit/<str:uuid>/', finale_invoice_edit, name='finale_invoice_edit'),
    # ])),
    # path('sales-order/', include([
    #     path('', sales_order_list, name='sales_order_list'),
    #     path('add/', sales_order_add, name='sales_order_add'),
    #     path('edit/<str:uuid>/', sales_order_edit, name='sales_order_edit'),
    # ])),
    # path('purchase-order/', include([
    #     path('', purchase_order_list, name='purchase_order_list'),
    #     path('add/', purchase_order_add, name='purchase_order_add'),
    #     path('edit/<str:uuid>/', purchase_order_edit, name='purchase_order_edit'),
    # ])),
    # path('manufacturer-invoice/', include([
    #     path('', manufacturer_invoice_list, name='manufacturer_invoice_list'),
    # ])),
]
