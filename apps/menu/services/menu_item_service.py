from apps.base.service import BaseModelService
from apps.inventory.services.product_service import ProductService
from apps.menu.services.menu_service import MenuService

from ..models.menu_item import MenuItem


class MenuItemService(BaseModelService):
    model = MenuItem
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu_service = self.get_menu_service()
        self.product_service = self.get_product_service()

    def get_menu_service(self):
        return MenuService()

    def get_product_service(self):
        return ProductService()

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = []

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if "menu_uuid" in kwargs:
            menu = self.menu_service.read_by_uuid(uuid_value=kwargs["menu_uuid"])
            kwargs["menu_id"] = menu.id
            del kwargs["menu_uuid"]

        if "item_uuid" in kwargs:
            item = self.product_service.read_by_uuid(uuid_value=kwargs["item_uuid"])
            kwargs["item_id"] = item.id
            del kwargs["item_uuid"]

        return kwargs, m2m_data

    def create_menu_item(self, **kwargs):
        remove_keys = []
        for key in remove_keys:
            del kwargs[key]
        kwargs, m2m_data = self.validated_data(**kwargs)
        return self.create(**kwargs)

    def update_menu_item(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance
