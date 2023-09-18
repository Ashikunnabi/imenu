from apps.base.service import BaseModelService

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
