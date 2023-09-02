from django.urls import include, path
from .views import *


app_name = "table"

urlpatterns = [
    path("api/", include("apps.table.api.urls"), name="api"),
]
