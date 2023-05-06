from django.urls import include, path
from .views import *


app_name = 'admin_others'

urlpatterns = [
    path('others/', include([
        path('product-image', product_image_list, name='product_image_list'),
        path('expense-type', expense_type_list, name='expense_type_list'),
        path('expense', expense_list, name='expense_list'),
    ])),
    
    path('expense/', include([
        path('', expense_list, name='expense_list'),
        path('add/', expense_add, name='expense_add'),
        path('edit/<str:uuid>/', expense_edit, name='expense_edit'),
    ])),
]
