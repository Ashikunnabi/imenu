from django.urls import include, path

app_name = "apps"


urlpatterns = [
    path("", include("apps.authentication.urls")),
    path("", include("apps.base.urls")),
    path("", include("apps.rbac.urls")),
    path("", include("apps.send_email.urls")),
    path("", include("apps.inventory.urls")),
    path("", include("apps.menu.urls")),
    path("", include("apps.table.urls")),
]
