from django.urls import include, path

from .views import *

app_name = "admin_inventory"

urlpatterns = [
    path(
        "attribute-groups/",
        include(
            [
                path("", attribute_group_list, name="attribute_group_list"),
                path("add/", attribute_group_add, name="attribute_group_add"),
                path("edit/<str:uuid>/", attribute_group_edit, name="attribute_group_edit"),
            ]
        ),
    ),
    path(
        "attributes/",
        include(
            [
                path("", attribute_list, name="attribute_list"),
                path("add/", attribute_add, name="attribute_add"),
                path("edit/<str:uuid>/", attribute_edit, name="attribute_edit"),
            ]
        ),
    ),
    path(
        "brands/",
        include(
            [
                path("", brand_list, name="brand_list"),
                path("add/", brand_add, name="brand_add"),
                path("edit/<str:uuid>/", brand_edit, name="brand_edit"),
            ]
        ),
    ),
    path(
        "documents/",
        include(
            [
                path("", document_list, name="document_list"),
                path("add/", document_add, name="document_add"),
                path("edit/<str:uuid>/", document_edit, name="document_edit"),
            ]
        ),
    ),
    path(
        "groups/",
        include(
            [
                path("", group_list, name="group_list"),
                path("add/", group_add, name="group_add"),
                path("edit/<str:uuid>/", group_edit, name="group_edit"),
            ]
        ),
    ),
    path(
        "products/",
        include(
            [
                path("", product_list, name="product_list"),
                path("add/", product_add, name="product_add"),
                path("edit/<str:uuid>/", product_edit, name="product_edit"),
            ]
        ),
    ),
    path(
        "types/",
        include(
            [
                path("", type_list, name="type_list"),
                path("add/", type_add, name="type_add"),
                path("edit/<str:uuid>/", type_edit, name="type_edit"),
            ]
        ),
    ),
    path(
        "suppliers/",
        include(
            [
                path("", supplier_list, name="supplier_list"),
                path("add/", supplier_add, name="supplier_add"),
                path("edit/<str:uuid>/", supplier_edit, name="supplier_edit"),
            ]
        ),
    ),
    path(
        "warehouses/",
        include(
            [
                path("", warehouse_list, name="warehouse_list"),
                path("add/", warehouse_add, name="warehouse_add"),
                path("edit/<str:uuid>/", warehouse_edit, name="warehouse_edit"),
            ]
        ),
    ),
    path(
        "units/",
        include(
            [
                path("", unit_list, name="unit_list"),
                path("add/", unit_add, name="unit_add"),
                path("edit/<str:uuid>/", unit_edit, name="unit_edit"),
            ]
        ),
    ),
    path(
        "vats/",
        include(
            [
                path("", vat_list, name="vat_list"),
                path("add/", vat_add, name="vat_add"),
                path("edit/<str:uuid>/", vat_edit, name="vat_edit"),
            ]
        ),
    ),
]
