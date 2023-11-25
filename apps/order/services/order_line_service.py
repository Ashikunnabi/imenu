import decimal

from apps.base.service import BaseModelService
from apps.inventory.services import ProductPriceService, ProductService

from ..models import OrderLine


class OrderLineService(BaseModelService):
    model = OrderLine
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_service = self.get_product_service()

    def get_product_service(self):
        return ProductService()

    def get_order_service(self):
        from apps.order.services.order_service import OrderService

        return OrderService()

    def get_product_price_service(self):
        return ProductPriceService()

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = ["permissions", "users"]

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if "order_uuid" in kwargs:
            order = self.get_order_service().read_by_uuid(
                uuid_value=kwargs.pop("order_uuid")
            )
            kwargs["order_id"] = order.id

        if "product_uuid" in kwargs:
            product = self.product_service.read_by_uuid(
                uuid_value=kwargs.pop("product_uuid")
            )
            kwargs["product_id"] = product.id

        # Default price
        kwargs["price_in_vat"] = decimal.Decimal("00.00")
        kwargs["price_ex_vat"] = decimal.Decimal("00.00")
        kwargs["total_price_in_vat"] = decimal.Decimal("00.00")
        kwargs["total_price_ex_vat"] = decimal.Decimal("00.00")
        return kwargs, m2m_data

    def create_order_line(self, **kwargs):
        data, m2m_data = self.validated_data(**kwargs)

        # check object already exists
        self.does_object_already_exists(**data)

        order_line = self.create(**data)
        return order_line

    def update_order_line(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance
