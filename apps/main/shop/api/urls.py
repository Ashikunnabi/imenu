from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('v1/', include('apps.main.shop.api.v1.urls'))
]
