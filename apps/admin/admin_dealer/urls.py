from django.urls import include, path
from .views import *


app_name = 'admin_dealer'

urlpatterns = [
    path('dealer/', include([
        path('', dealer_list, name='dealer_list'),
        path('edit/<str:uuid>/', dealer_edit, name='dealer_edit'),
    ])),
]
