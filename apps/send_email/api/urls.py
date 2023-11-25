from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('v1/', include('apps.send_email.api.v1.urls'))
]
