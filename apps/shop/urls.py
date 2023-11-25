from django.urls import include, path
from .views import *


app_name = 'shop'


urlpatterns = [
    path('api/', include('apps.shop.api.urls'))
]