from django.urls import include, path

from .views import *

app_name = "admin_table"

urlpatterns = [
    path(
        "table-types/",
        include(
            [
                path("", table_type_list, name="table_type_list"),
                path("add/", table_type_add, name="table_type_add"),
                path("edit/<str:uuid>/", table_type_edit, name="table_type_edit"),
            ]
        ),
    ),
    path(
        "tables/",
        include(
            [
                path("", table_list, name="table_list"),
                path("add/", table_add, name="table_add"),
                path("edit/<str:uuid>/", table_edit, name="table_edit"),
            ]
        ),
    ),
]
