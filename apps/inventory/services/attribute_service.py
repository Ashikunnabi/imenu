from apps.base.service import BaseModelService
from .attribute_group_service import AttributeGroupService

from ..models import Attribute


class AttributeService(BaseModelService):
    model = Attribute
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_attribute_group_service(self):
        return AttributeGroupService()

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = ["permissions", "users"]

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if "attribute_group_uuid" in kwargs:
            attribute_group = self.get_attribute_group_service().read_by_uuid(
                uuid_value=kwargs.pop("attribute_group_uuid")
            )
            kwargs["attribute_group_id"] = attribute_group.id

        return kwargs, m2m_data

    def create_attribute(self, **kwargs):
        data, m2m_data = self.validated_data(**kwargs)

        # check object already exists
        self.does_object_already_exists(**data)
        return self.create(**data)

    def update_attribute(self, instance, **kwargs):
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
