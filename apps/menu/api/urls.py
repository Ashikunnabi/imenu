from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('v1/menu/', include('apps.menu.api.v1.urls'))
]
