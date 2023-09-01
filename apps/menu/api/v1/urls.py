from django.urls import path

from .viewsets import (
    MenuItemListCreateAPIView,
    MenuItemRetrieveUpdateDestroyAPIView,
    MenuListCreateAPIView,
    MenuRetrieveUpdateDestroyAPIView,
    MenuTypeListCreateAPIView,
    MenuTypeRetrieveUpdateDestroyAPIView,
)

app_name = "v1"

urlpatterns = [
    path(
        "menu-types/",
        MenuTypeListCreateAPIView.as_view(),
        name="menu_type-list-create",
    ),
    path(
        "menu-types/<uuid:uuid>/",
        MenuTypeRetrieveUpdateDestroyAPIView.as_view(),
        name="menu_type-retrieve-update-delete",
    ),
    path(
        "menus/",
        MenuListCreateAPIView.as_view(),
        name="menu-list-create",
    ),
    path(
        "menus/<uuid:uuid>/",
        MenuRetrieveUpdateDestroyAPIView.as_view(),
        name="menu-retrieve-update-delete",
    ),
    path(
        "menu-items/",
        MenuItemListCreateAPIView.as_view(),
        name="menu_item-list-create",
    ),
    path(
        "menu-items/<uuid:uuid>/",
        MenuItemRetrieveUpdateDestroyAPIView.as_view(),
        name="menu_item-retrieve-update-delete",
    ),
]
