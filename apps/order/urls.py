from django.urls import include, path
from .views import *


app_name = 'order'

urlpatterns = [
    path('api/', include('apps.order.api.urls'), name='api'),
]
