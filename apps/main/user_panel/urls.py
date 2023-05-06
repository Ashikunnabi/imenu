from django.urls import include, path
from .views import *


app_name = 'user_panel'

urlpatterns = [
    path('my-account/', my_account, name='my_account'),
    path('my-cart/', my_cart, name='my_cart'),
    path('orders-cancellations/', orders_cancellations, name='orders_cancellations'),
    path('my-sales-reps/', my_sales_reps, name='my_sales_reps'),
    path('invoice/', finale_invoice, name='finale_invoice'),
    path('return/', return_order, name='return'),
    path('api/', include('apps.main.user_panel.api.urls'), name='api'),
]
