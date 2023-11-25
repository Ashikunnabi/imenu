from django.urls import include, path


app_name = "dashboard_api"

urlpatterns = [path("v1/dashboard/table/", include("apps.table.dashboard_api.v1.urls"))]
