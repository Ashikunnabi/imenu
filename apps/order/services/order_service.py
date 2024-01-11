from apps.base.service import BaseModelService
from apps.cart.services.cart_service import CartService
from apps.order.mappers.cart_to_order_mapper import (
    CartLineToOrderLineMapper,
    CartToOrderMapper,
)

from ..models import Order
from .order_line_service import OrderLineService


class OrderService(BaseModelService):
    model = Order
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_line_service = self.get_order_line_service()

    def get_order_line_service(self):
        return OrderLineService()

    @property
    def cart_service(self):
        return CartService()

    @property
    def cart_to_order_mapper(self):
        return CartToOrderMapper()

    @property
    def cart_line_to_order_line_mapper(self):
        return CartLineToOrderLineMapper()

    def create_order_from_cart(self, cart_uuid, **kwargs):
        cart = self.cart_service.read_by_uuid(cart_uuid)
        order = self.cart_to_order_mapper.map(cart)
        order.save()

        # order line create
        for line in cart.lines.all():
            order_line = self.cart_line_to_order_line_mapper.map(order, line)
            order_line.save()
        return order

    def create_order(self, **kwargs):
        order = self.create_order_from_cart(cart_uuid=kwargs.get("cart_uuid"))
        return order
