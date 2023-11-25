from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('v1/orders/', include('apps.order.api.v1.urls'))
]
