from apps.base.service import BaseModelService

from ..models import ProductAttribute
from .attribute_service import AttributeService
from .product_service import ProductService


class ProductAttributeService(BaseModelService):
    model = ProductAttribute
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_product_service(self):
        return ProductService()

    def get_attribute_service(self):
        return AttributeService()

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

        if "attribute_uuid" in kwargs:
            attribute = self.get_attribute_service().read_by_uuid(
                uuid_value=kwargs.pop("attribute_uuid")
            )
            kwargs["attribute_id"] = attribute.id

        if "name" in kwargs:
            kwargs["attribute_id"] = (
                self.get_attribute_service()
                .create_attribute(
                    **{
                        "name": kwargs.pop("name"),
                        "attribute_group_uuid": kwargs.pop("attribute_group_uuid"),
                    }
                )
                .id
            )

        return kwargs, m2m_data

    def create_product_attribute(self, **kwargs):
        data, m2m_data = self.validated_data(**kwargs)

        # check object already exists
        self.does_object_already_exists(**data)
        return self.create(**data)

    def update_product_attribute(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)

        if "permissions" in m2m_data:
            if m2m_data.get("permissions"):
                instance.permissions.set(m2m_data.get("permissions"))
            else:
                instance.permissions.clear()
        if "users" in m2m_data:
            if m2m_data.get("users"):
                instance.user_set.set(m2m_data.get("users"))
            else:
                instance.user_set.clear()
        return instance
