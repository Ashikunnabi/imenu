from django.urls import include, path
from .views import *


app_name = 'admin_shop'

urlpatterns = [
    path('shop/', include([
        path('', shop_list, name='shop_list'),
        path('add/', shop_add, name='shop_add'),
        path('edit/<str:uuid>/', shop_edit, name='shop_edit'),
        path('pos/', shop_pos, name='shop_pos'),
    ])),
]
