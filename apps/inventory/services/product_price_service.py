from apps.base.service import BaseModelService

from ..models import ProductPrice
from .product_service import ProductService


class ProductPriceService(BaseModelService):
    model = ProductPrice
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_product_service(self):
        return ProductService()

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

    def create_product_price(self, **kwargs):
        data, m2m_data = self.validated_data(**kwargs)
        return self.create(**data)

    def update_product_price(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance
