from django.urls import path

from .viewsets import (
    TableCodeListCreateAPIView,
    TableCodeQRCodeCreateAPIView,
    TableCodeRetrieveUpdateDestroyAPIView,
    TableDocumentListCreateAPIView,
    TableDocumentRetrieveUpdateDestroyAPIView,
    TableDocumentUploadAPIView,
    TableListCreateAPIView,
    TableRetrieveUpdateDestroyAPIView,
    TableTypeListCreateAPIView,
    TableTypeRetrieveUpdateDestroyAPIView,
)

app_name = "v1"

urlpatterns = [
    path(
        "table-types/",
        TableTypeListCreateAPIView.as_view(),
        name="table_type_list_create",
    ),
    path(
        "table-types/<uuid:uuid>/",
        TableTypeRetrieveUpdateDestroyAPIView.as_view(),
        name="table_type_retrieve_update_delete",
    ),
    path(
        "tables/",
        TableListCreateAPIView.as_view(),
        name="table_list_create",
    ),
    path(
        "tables/<uuid:uuid>/",
        TableRetrieveUpdateDestroyAPIView.as_view(),
        name="table_retrieve_update_delete",
    ),
    path(
        "tables/<uuid:table_uuid>/codes/",
        TableCodeListCreateAPIView.as_view(),
        name="table_code_list_create",
    ),
    path(
        "tables/<uuid:table_uuid>/codes/<uuid:uuid>/",
        TableCodeRetrieveUpdateDestroyAPIView.as_view(),
        name="table_code_retrieve_update_delete",
    ),
    path(
        "tables/<uuid:table_uuid>/codes/<uuid:uuid>/create-qr-code/",
        TableCodeQRCodeCreateAPIView.as_view(),
        name="table-code-create-qr-code",
    ),
    path(
        "tables/<uuid:table_uuid>/documents/",
        TableDocumentListCreateAPIView.as_view(),
        name="table_document_list_create",
    ),
    path(
        "tables/<uuid:table_uuid>/documents/<uuid:uuid>/",
        TableDocumentRetrieveUpdateDestroyAPIView.as_view(),
        name="table_document_retrieve_update_delete",
    ),
    path(
        "tables/<uuid:table_uuid>/upload-document/",
        TableDocumentUploadAPIView.as_view(),
        name="table_document_upload",
    ),
]
