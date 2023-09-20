from apps.base.service import BaseModelService
from apps.document_generation.services.upload_document_service import UploadDocumentService
from apps.table.services.table_document_service import TableDocumentService

from ..models.table import Table


class TableService(BaseModelService):
    model = Table
    search_keywords = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_type_service = self.get_table_type_service()

    def get_table_type_service(self):
        from apps.table.services import TableTypeService

        return TableTypeService()

    def get_upload_document_service(self, file_path):
        return UploadDocumentService(file_path=file_path)

    def get_table_document_service(self):
        return TableDocumentService()

    def get_table_type(self, uuid):
        table_type = self.table_type_service.read_by_uuid(uuid_value=uuid)
        return table_type

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = []

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if "type_uuid" in kwargs:
            kwargs["type_id"] = self.get_table_type(uuid=kwargs["type_uuid"]).id
            del kwargs["type_uuid"]

        return kwargs, m2m_data

    def create_table(self, **kwargs):
        remove_keys = []
        for key in remove_keys:
            del kwargs[key]
        kwargs, m2m_data = self.validated_data(**kwargs)
        return self.create(**kwargs)

    def update_table(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance


    def upload_document(self, *args, **kwargs):
        table_uuid = kwargs["table_uuid"]
        table = self.read_by_uuid(uuid_value=table_uuid)
        file_path = f"tables/{table_uuid}/"

        upload_document_service = self.get_upload_document_service(file_path=file_path)
        table_document_service = self.get_table_document_service()
        document = upload_document_service.save_file_in_storage(file=kwargs["file"])

        # save data into ProductDocument model
        table_document_data = {
            "table_id": table.id,
            "document_id": document.id,
            "sort_order": kwargs.get("sort_order", 0),
        }
        table_document = table_document_service.create_table_document(
            **table_document_data
        )

        return table_document
