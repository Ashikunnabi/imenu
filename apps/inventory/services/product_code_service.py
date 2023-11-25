from apps.base.service import BaseModelService
from apps.base.utils.basic import build_media_url
from apps.document_generation.services import QRCodeService
from apps.inventory.constants import ProductDocumentTypes
from apps.inventory.services.document_service import DocumentService

from ..models import ProductCode
from .product_document_service import ProductDocumentService
from .product_service import ProductService


class ProductCodeService(BaseModelService):
    model = ProductCode
    search_keywords = ["type", "value"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_product_service(self):
        return ProductService()

    def get_document_service(self):
        return DocumentService()

    def get_product_document_service(self):
        return ProductDocumentService()

    def get_qr_code_service(self):
        return QRCodeService()

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = ["permissions", "users"]

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if "product_uuid" in kwargs:
            product = self.get_product_service().read_by_uuid(
                uuid_value=kwargs.pop("product_uuid")
            )
            kwargs["product_id"] = product.id

        return kwargs, m2m_data

    def create_product_code(self, **kwargs):
        data, m2m_data = self.validated_data(**kwargs)

        # check object already exists
        self.does_object_already_exists(**data)
        return self.create(**data)

    def update_product_code(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance

    def generate_qr_code(self, *args, **kwargs):
        product_code_uuid = kwargs["uuid"]
        data = kwargs["data"]

        document_service = self.get_document_service()
        product_document_service = self.get_product_document_service()
        qr_code_service = self.get_qr_code_service()
        product_code = self.read_by_uuid(uuid_value=product_code_uuid)

        # generate qr code
        qr_code_service.data = data
        dir_path = f"products/{product_code.product.uuid}"
        qr_code_service.file_path = (
            f"{dir_path}/{product_code.type}_{product_code.uuid}.png"
        )
        qr_code_file_path = qr_code_service.generate_and_save_in_storage()

        # save data into Document model
        document = document_service.create_document(**{"path": qr_code_file_path})
        # save data into ProductDocument model
        product_document_data = {
            "product_id": product_code.product_id,
            "document_id": document.id,
            "type": ProductDocumentTypes.QRCODE,
        }
        product_document_service.create_product_document(**product_document_data)

        return build_media_url(qr_code_file_path)

    def get_qr_code(self, product_code_uuid, *args, **kwargs):
        qr_code_file_path = None
        product_code = self.read_by_uuid(uuid_value=product_code_uuid)
        product_document_service = self.get_product_document_service()

        data = {
            "type": ProductDocumentTypes.QRCODE,
            "product_id": product_code.product_id,
        }
        product_documents = product_document_service.list(**data)
        if product_documents:
            pattern = f"{product_code.type}_{product_code.uuid}"
            product_documents = product_documents.filter(
                document__name__startswith=pattern
            )
        if product_documents:
            qr_code_file_path = product_documents.last().document.file
            qr_code_file_path = build_media_url(qr_code_file_path)

        return qr_code_file_path

    def detail_response(self, product_code):
        product_code.qr_code_path = self.get_qr_code(product_code.uuid)
        return product_code

    def list_response(self, product_codes):
        data = []

        for product_code in product_codes:
            data.append(self.detail_response(product_code))
        return data
