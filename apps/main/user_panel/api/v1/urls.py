from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .viewsets import *


app_name = 'v1'


router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'sales-reps', SalesRepsViewSet, basename='sales_reps')
router.register(r'finale-invoice', FinaleInvoiceViewSet, basename='finale_invoice')
router.register(r'manufacturer-invoice', ManufacturerInvoiceViewSet, basename='manufacturer_invoice')
router.register(r'sales-order', SalesOrderViewSet, basename='sales_order')
router.register(r'purchase-order', PurchaseOrderViewSet, basename='purchase_order')
router.register(r'invoice-order', InvoiceOrderViewSet, basename='invoice_order')
router.register(r'expense-type', ExpenseTypeViewSet, basename='expense_type')
router.register(r'expense', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('', include(router.urls)),
]
