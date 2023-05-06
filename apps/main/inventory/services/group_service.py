from apps.core.base.service import BaseModelService
from apps.main.inventory.exceptions import GroupParentSameObjectException

from ..models import Group


class GroupService(BaseModelService):
    model = Group
    search_keywords = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = ["permissions", "users"]

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if "parent_uuid" in kwargs:
            group = self.read_by_uuid(uuid_value=kwargs.pop("parent_uuid"))
            kwargs["parent_id"] = group.id

        return kwargs, m2m_data

    def create_group(self, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        return self.create(**kwargs)

    def update_group(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        
        if instance.id == kwargs.get("parent_id"):
            raise GroupParentSameObjectException
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
