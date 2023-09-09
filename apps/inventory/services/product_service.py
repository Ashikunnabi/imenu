from apps.base.service import BaseModelService
from apps.base.utils.basic import build_media_url
from apps.document_generation.services.qr_code_service import QRCodeService
from apps.inventory.constants import ProductDocumentTypes
from apps.document_generation.services.upload_document_service import (
    UploadDocumentService,
)
from apps.inventory.services.brand_service import BrandService
from apps.inventory.services.document_service import DocumentService
from apps.inventory.services.group_service import GroupService
from apps.inventory.services.product_document_service import ProductDocumentService
from apps.inventory.services.type_service import TypeService

from ..models import Product


class ProductService(BaseModelService):
    model = Product
    search_keywords = ["code", "name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_upload_document_service(self, file_path):
        return UploadDocumentService(file_path=file_path)

    def get_brand_service(self):
        return BrandService()

    def get_document_service(self):
        return DocumentService()

    def get_group_service(self):
        return GroupService()

    def get_type_service(self):
        return TypeService()

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

        if "parent_uuid" in kwargs:
            parent = self.read_by_uuid(uuid_value=kwargs.pop("parent_uuid"))
            kwargs["parent_id"] = parent.id

        if "brand_uuid" in kwargs:
            brand = self.get_brand_service().read_by_uuid(
                uuid_value=kwargs.pop("brand_uuid")
            )
            kwargs["brand_id"] = brand.id

        if "group_uuid" in kwargs:
            group = self.get_group_service().read_by_uuid(
                uuid_value=kwargs.pop("group_uuid")
            )
            kwargs["group_id"] = group.id

        if "type_uuid" in kwargs:
            _type = self.get_type_service().read_by_uuid(
                uuid_value=kwargs.pop("type_uuid")
            )
            kwargs["type_id"] = _type.id

        return kwargs, m2m_data

    def create_product(self, **kwargs):
        data, m2m_data = self.validated_data(**kwargs)

        # check object already exists
        self.does_object_already_exists(**data)
        return self.create(**data)

    def update_product(self, instance, **kwargs):
        data, m2m_data = self.validated_data(**kwargs)
        return self.update_model_instance(instance, **data)

    def generate_qr_code(self, *args, **kwargs):
        product_uuid = kwargs["uuid"]
        data = kwargs["data"]

        document_service = self.get_document_service()
        product_document_service = self.get_product_document_service()
        qr_code_service = self.get_qr_code_service()
        product = self.read_by_uuid(uuid_value=product_uuid)

        # generate qr code
        qr_code_service.data = data
        dir_path = f"products/{product.uuid}"
        qr_code_service.file_path = f"{dir_path}/code_{product.uuid}.png"
        qr_code_file_path = qr_code_service.generate_and_save_in_storage()

        # save data into Document model
        document = document_service.create_document(**{"path": qr_code_file_path})
        # save data into ProductDocument model
        product_document_data = {
            "product_id": product.id,
            "document_id": document.id,
            "type": ProductDocumentTypes.QRCODE,
        }
        product_document_service.create_product_document(**product_document_data)

        return build_media_url(qr_code_file_path)

    def get_qr_code(self, product_uuid, *args, **kwargs):
        qr_code_file_path = None
        product = self.read_by_uuid(uuid_value=product_uuid)
        product_document_service = self.get_product_document_service()

        data = {
            "type": ProductDocumentTypes.QRCODE,
            "product_id": product.id,
        }
        product_documents = product_document_service.list(**data)
        if product_documents:
            pattern = f"code_{product.uuid}"
            product_documents = product_documents.filter(
                document__name__startswith=pattern
            )
        if product_documents:
            qr_code_file_path = product_documents.last().document.file.url
            qr_code_file_path = build_media_url(qr_code_file_path)

        return qr_code_file_path

    def product_search_single_response(self, product):
        data = {
            "uuid": product.uuid,
            "name": product.name,
            "brand": product.brand,
            "code": product.code,
            "description": product.description,
            "short_description": product.short_description,
            "family": product.family,
            "series": product.series,
            "group": product.group,
            "is_active": product.is_active,
            "parent": self.product_search_single_response(product.parent)
            if product.parent
            else None,
            "type": product.type,
            "documents": product.documents,
            "prices": product.prices,
        }
        return data

    def product_search_list_response(self, queryset):
        data = []
        for product in queryset:
            temp_dict = self.product_search_single_response(product)
            data.append(temp_dict)
        return data

    def upload_document(self, *args, **kwargs):
        product_uuid = kwargs["product_uuid"]
        product = self.read_by_uuid(uuid_value=product_uuid)
        file_path = f"products/{product_uuid}/"

        upload_document_service = self.get_upload_document_service(file_path=file_path)
        product_document_service = self.get_product_document_service()
        document = upload_document_service.save_file_in_storage(file=kwargs["file"])

        # save data into ProductDocument model
        product_document_data = {
            "product_id": product.id,
            "document_id": document.id,
            "sort_order": kwargs.get("sort_order", 0),
        }
        product_document = product_document_service.create_product_document(
            **product_document_data
        )

        return product_document
