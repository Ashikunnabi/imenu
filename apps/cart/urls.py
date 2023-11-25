from django.urls import include, path
from .views import *


app_name = 'cart'

urlpatterns = [
    path('api/', include('apps.cart.api.urls'), name='api'),
]
