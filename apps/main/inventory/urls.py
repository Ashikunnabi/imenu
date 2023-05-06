from django.urls import include, path
from .views import *


app_name = 'inventory'

urlpatterns = [
    path('api/', include('apps.main.inventory.api.urls'), name='api'),
]
