from apps.core.base.service import BaseModelService
from apps.main.inventory.services.product_service import ProductService
from apps.main.inventory.services.unit_service import UnitService

from ..models import ProductUnit


class ProductUnitService(BaseModelService):
    model = ProductUnit
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_product_service(self):
        return ProductService()

    def get_unit_service(self):
        return UnitService()

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

        if "unit_uuid" in kwargs:
            unit = self.get_unit_service().read_by_uuid(
                uuid_value=kwargs.pop("unit_uuid")
            )
            kwargs["unit_id"] = unit.id

        return kwargs, m2m_data

    def create_product_unit(self, **kwargs):
        data, m2m_data = self.validated_data(**kwargs)

        # check object already exists
        self.does_object_already_exists(**data)
        return self.create(**data)

    def update_product_unit(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance
