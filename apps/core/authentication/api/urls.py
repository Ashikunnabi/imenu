from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('v1/', include('apps.core.authentication.api.v1.urls'))
]
