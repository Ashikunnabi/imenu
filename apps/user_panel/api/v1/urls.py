from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .viewsets import *


app_name = 'v1'


router = DefaultRouter()
router.Register(r'cart', CartViewSet, basename='cart')
router.Register(r'order', OrderViewSet, basename='order')
router.Register(r'sales-reps', SalesRepsViewSet, basename='sales_reps')
router.Register(r'finale-invoice', FinaleInvoiceViewSet, basename='finale_invoice')
router.Register(r'manufacturer-invoice', ManufacturerInvoiceViewSet, basename='manufacturer_invoice')
router.Register(r'sales-order', SalesOrderViewSet, basename='sales_order')
router.Register(r'purchase-order', PurchaseOrderViewSet, basename='purchase_order')
router.Register(r'invoice-order', InvoiceOrderViewSet, basename='invoice_order')
router.Register(r'expense-type', ExpenseTypeViewSet, basename='expense_type')
router.Register(r'expense', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('', include(router.urls)),
]
