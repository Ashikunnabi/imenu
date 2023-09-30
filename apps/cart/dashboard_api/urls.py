from django.urls import include, path


app_name = 'dashboard_api'

urlpatterns = [
    path('v1/dashboard/carts/', include('apps.cart.dashboard_api.v1.urls'))
]
