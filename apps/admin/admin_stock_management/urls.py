from django.urls import include, path
from .views import *


app_name = 'admin_stock_management'

urlpatterns = [
    path('sales-order/', include([
        path('', sales_order_list, name='sales_order_list'),
        path('add/', sales_order_add, name='sales_order_add'),
        path('edit/<str:uuid>/', sales_order_edit, name='sales_order_edit'),
    ])),
    path('purchase-order/', include([
        path('', purchase_order_list, name='purchase_order_list'),
        path('add/', purchase_order_add, name='purchase_order_add'),
        path('edit/<str:uuid>/', purchase_order_edit, name='purchase_order_edit'),
    ])),
    path('stock-transaction/', include([
        path('', stock_transaction_list, name='stock_transaction_list'),
        path('add/', stock_transaction_add, name='stock_transaction_add'),
        path('edit/<str:uuid>/', stock_transaction_edit, name='stock_transaction_edit'),
    ])),
]
