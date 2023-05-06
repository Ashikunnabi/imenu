from django.urls import include, path
from .views import *


app_name = 'admin_pos'

urlpatterns = [
    path('pos/', include([
        path('', product_image_list, name='product_image_list'),
    ])),
]
