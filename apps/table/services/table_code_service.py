from apps.base.service import BaseModelService
from apps.base.utils.basic import build_media_url
from apps.document_generation.services import QRCodeService
from apps.inventory.services.document_service import DocumentService

from ..constants import TableDocumentTypes
from ..models import TableCode
from .table_document_service import TableDocumentService
from .table_service import TableService


class TableCodeService(BaseModelService):
    model = TableCode
    search_keywords = ["type", "value"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_table_service(self):
        return TableService()

    def get_document_service(self):
        return DocumentService()

    def get_table_document_service(self):
        return TableDocumentService()

    def get_qr_code_service(self):
        return QRCodeService()

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = ["permissions", "users"]

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if "table_uuid" in kwargs:
            table = self.get_table_service().read_by_uuid(
                uuid_value=kwargs.pop("table_uuid")
            )
            kwargs["table_id"] = table.id

        return kwargs, m2m_data

    def create_table_code(self, **kwargs):
        data, m2m_data = self.validated_data(**kwargs)

        # check object already exists
        self.does_object_already_exists(**data)
        return self.create(**data)

    def update_table_code(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance

    def generate_qr_code(self, *args, **kwargs):
        table_code_uuid = kwargs["uuid"]
        data = kwargs["data"]

        document_service = self.get_document_service()
        table_document_service = self.get_table_document_service()
        qr_code_service = self.get_qr_code_service()
        table_code = self.read_by_uuid(uuid_value=table_code_uuid)

        # generate qr code
        qr_code_service.data = data
        dir_path = f"tables/{table_code.table.uuid}"
        qr_code_service.file_path = (
            f"{dir_path}/{table_code.type}_{table_code.uuid}.png"
        )
        qr_code_file_path = qr_code_service.generate_and_save_in_storage()

        # save data into Document model
        document = document_service.create_document(**{"path": qr_code_file_path})
        # save data into TableDocument model
        table_document_data = {
            "table_id": table_code.table_id,
            "document_id": document.id,
            "type": TableDocumentTypes.QRCODE,
        }
        table_document_service.create_table_document(**table_document_data)

        return build_media_url(qr_code_file_path)

    def get_qr_code(self, table_code_uuid, *args, **kwargs):
        qr_code_file_path = None
        table_code = self.read_by_uuid(uuid_value=table_code_uuid)
        table_document_service = self.get_table_document_service()

        data = {
            "type": TableDocumentTypes.QRCODE,
            "table_id": table_code.table_id,
        }
        table_documents = table_document_service.list(**data)
        if table_documents:
            pattern = f"{table_code.type}_{table_code.uuid}"
            table_documents = table_documents.filter(document__name__startswith=pattern)
        if table_documents:
            qr_code_file_path = table_documents.last().document.file.url
            qr_code_file_path = build_media_url(qr_code_file_path)

        return qr_code_file_path

    def detail_response(self, table_code):
        table_code.qr_code_path = self.get_qr_code(table_code.uuid)
        return table_code

    def list_response(self, table_codes):
        data = []

        for table_code in table_codes:
            data.append(self.detail_response(table_code))
        return data
