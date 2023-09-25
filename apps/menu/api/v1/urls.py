from django.urls import path

from .viewsets import (
    MenuDocumentListCreateAPIView,
    MenuDocumentRetrieveUpdateDestroyAPIView,
    MenuDocumentUploadAPIView,
    MenuItemListCreateAPIView,
    MenuItemRetrieveUpdateDestroyAPIView,
    MenuListAPIView,
    MenuRetrieveUpdateDestroyAPIView,
    MenuTypeListCreateAPIView,
    MenuTypeRetrieveUpdateDestroyAPIView,
)

app_name = "v1"

urlpatterns = [
    path(
        "menu-types/",
        MenuTypeListCreateAPIView.as_view(),
        name="menu_type_list_create",
    ),
    path(
        "menu-types/<uuid:uuid>/",
        MenuTypeRetrieveUpdateDestroyAPIView.as_view(),
        name="menu_type_retrieve_update_delete",
    ),
    path(
        "",
        MenuListAPIView.as_view(),
        name="menu_list",
    ),
    path(
        "<uuid:uuid>/",
        MenuRetrieveUpdateDestroyAPIView.as_view(),
        name="menu_retrieve_update_delete",
    ),
    path(
        "menu-items/",
        MenuItemListCreateAPIView.as_view(),
        name="menu_item_list_create",
    ),
    path(
        "menu-items/<uuid:uuid>/",
        MenuItemRetrieveUpdateDestroyAPIView.as_view(),
        name="menu_item_retrieve_update_delete",
    ),
    path(
        "<uuid:menu_uuid>/documents/",
        MenuDocumentListCreateAPIView.as_view(),
        name="menu_document_list_create",
    ),
    path(
        "<uuid:menu_uuid>/documents/<uuid:uuid>/",
        MenuDocumentRetrieveUpdateDestroyAPIView.as_view(),
        name="menu_document_retrieve_update_delete",
    ),
    path(
        "<uuid:menu_uuid>/upload-document/",
        MenuDocumentUploadAPIView.as_view(),
        name="menu_document_upload",
    ),
]
