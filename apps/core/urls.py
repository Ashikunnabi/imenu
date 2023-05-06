from django.urls import path, include


app_name = 'core'


urlpatterns = [
    path('', include('apps.core.authentication.urls')),
    path('', include('apps.core.base.urls')),
    path('', include('apps.core.rbac.urls')),
    path('', include('apps.core.send_email.urls')),
]
