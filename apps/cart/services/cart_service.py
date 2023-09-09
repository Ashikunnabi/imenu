import decimal
from django.db.models import Sum
from apps.base.service import BaseModelService
from apps.table.services.table_service import TableService

from ..models.cart import Cart
from .cart_line_service import CartLineService


class CartService(BaseModelService):
    model = Cart
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cart_line_service = self.get_cart_line_service()

    def get_cart_line_service(self):
        return CartLineService()

    def get_table_service(self):
        return TableService()

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = ["permissions", "users"]

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if "table_uuid" in kwargs:
            table = self.get_table_service().read_by_uuid(
                uuid_value=kwargs.pop("table_uuid")
            )
            kwargs["table_id"] = table.id

        # Default price
        kwargs["total_price_in_vat"] = decimal.Decimal("00.00")
        kwargs["total_price_ex_vat"] = decimal.Decimal("00.00")

        return kwargs, m2m_data

    def create_cart(self, **kwargs):
        data, m2m_data = self.validated_data(**kwargs)
        lines = data.pop("lines", [])

        cart = self.create(**data)

        # cart line create
        for line in lines:
            line["cart_id"] = cart.id
            self.cart_line_service.create_cart_line(**line)

        self.calculate_price(cart=cart)

        return cart

    def update_cart(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance

    def calculate_price(self, cart):
        lines = cart.lines.all()

        for line in lines:
            line.total_price_ex_vat = decimal.Decimal(line.quantity) * line.price_ex_vat
            line.total_price_in_vat = decimal.Decimal(line.quantity) * line.price_in_vat
            line.save()

        cart.refresh_from_db()
        lines = cart.lines.all()
        cart.total_price_ex_vat = lines.aggregate(sum=Sum("total_price_ex_vat")).get(
            "sum"
        ) or decimal.Decimal("0")
        cart.total_price_in_vat = lines.aggregate(sum=Sum("total_price_in_vat")).get(
            "sum"
        ) or decimal.Decimal("0")
        cart.save()
        return cart
