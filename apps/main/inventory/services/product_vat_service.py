from apps.core.base.service import BaseModelService
from apps.main.inventory.services.product_service import ProductService
from apps.main.inventory.services.vat_service import VatService

from ..models import ProductVat


class ProductVatService(BaseModelService):
    model = ProductVat
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_product_service(self):
        return ProductService()

    def get_vat_service(self):
        return VatService()

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

        if "vat_uuid" in kwargs:
            vat = self.get_vat_service().read_by_uuid(
                uuid_value=kwargs.pop("vat_uuid")
            )
            kwargs["vat_id"] = vat.id

        return kwargs, m2m_data

    def create_product_vat(self, **kwargs):
        data, m2m_data = self.validated_data(**kwargs)

        # check object already exists
        self.does_object_already_exists(**data)
        return self.create(**data)

    def update_product_vat(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance
