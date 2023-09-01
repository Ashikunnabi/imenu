from django.urls import include, path
from .views import *


app_name = 'menu'

urlpatterns = [
    path('api/', include('apps.menu.api.urls'), name='api'),
]
