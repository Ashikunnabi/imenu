from django.urls import include, path
from .views import *


app_name = 'inventory'

urlpatterns = [
    path('api/', include('apps.inventory.dashboard_api.urls'), name='dashboard_api'),
    path('api/', include('apps.inventory.api.urls'), name='api'),
]
