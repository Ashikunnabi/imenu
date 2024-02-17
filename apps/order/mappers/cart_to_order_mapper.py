from apps.cart.models.cart import Cart
from apps.cart.models.cart_line import CartLine
from apps.order.constants import OrderLineStatus, OrderStatus
from apps.order.models.order import Order
from apps.order.models.order_line import OrderLine


class CartToOrderMapper:
    def map(self, cart: Cart) -> Order:
        return Order(
            placed_by=cart.user,
            table=cart.table,
            total_price_ex_vat=cart.total_price_ex_vat,
            total_price_in_vat=cart.total_price_in_vat,
            extra_info=cart.extra_info,
            status=OrderStatus.ORDER_PLACED,
        )


class CartLineToOrderLineMapper:
    def map(self, order: Order, cart_line: CartLine) -> OrderLine:
        return OrderLine(
            order=order,
            product=cart_line.product,
            quantity=cart_line.quantity,
            price_ex_vat=cart_line.price_ex_vat,
            price_in_vat=cart_line.price_in_vat,
            total_price_ex_vat=cart_line.total_price_ex_vat,
            total_price_in_vat=cart_line.total_price_in_vat,
            extra_info=cart_line.extra_info,
            status=OrderLineStatus.ORDER_PLACED,
        )
