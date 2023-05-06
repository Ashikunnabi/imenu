from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('v1/inventory/', include('apps.main.inventory.api.v1.urls'))
]
