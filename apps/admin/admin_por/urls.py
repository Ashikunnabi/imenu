from django.urls import include, path
from .views import *


app_name = 'admin_por'

urlpatterns = [
    path('por/', include([
        path('', product_image_list, name='product_image_list'),
    ])),
]
