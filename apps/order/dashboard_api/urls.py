from django.urls import include, path


app_name = 'dashboard_api'

urlpatterns = [
    path('v1/orders/', include('apps.order.dashboard_api.v1.urls'))
]
