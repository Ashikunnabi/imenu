from django.urls import include, path
from .views import *


app_name = 'admin_user_panel'

urlpatterns = [
    path('sales-reps/', include([
        path('', sales_reps_list, name='sales_reps_list'),
        path('add/', sales_reps_add, name='sales_reps_add'),
        path('edit/<str:uuid>/', sales_reps_edit, name='sales_reps_edit'),
    ])),
]
