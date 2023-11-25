from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('v1/', include('apps.user_panel.api.v1.urls'))
]
