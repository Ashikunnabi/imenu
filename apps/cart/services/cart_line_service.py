import decimal
from apps.base.service import BaseModelService
from apps.inventory.services.product_service import ProductService

from ..models import CartLine


class CartLineService(BaseModelService):
    model = CartLine
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_service = self.get_product_service()

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

    def create_cart_line(self, **kwargs):
        data, m2m_data = self.validated_data(**kwargs)

        # check object already exists
        self.does_object_already_exists(**data)

        cart_line = self.create(**data)
        self.calculate_price(line=cart_line)
        return cart_line

    def update_cart_line(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        self.calculate_price(line=instance)
        return instance

    def calculate_price(self, line):
        line.price_ex_vat = decimal.Decimal("10")
        line.price_in_vat = decimal.Decimal("11")
        line.total_price_ex_vat = decimal.Decimal(line.quantity) * line.price_ex_vat
        line.total_price_in_vat = decimal.Decimal(line.quantity) * line.price_in_vat
        line.save()
        return line
