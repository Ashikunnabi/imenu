from django.db import transaction

from apps.core.base.utils.basic import fix_external_decimal_places

from .models import (
    ShopExtraLine,
    ShopExtraLineTypes,
    Shopkeeper,
    ShopOrder,
    ShopOrderLine,
    ShopOrderLineStatus,
    ShopOrderStatus,
    ShopProduct,
)


class ShopOrderProcess:
    def __init__(self, request_user_id, order=None) -> None:
        self.request_user_id = request_user_id
        self.order = order

    def add_orderline(self, product, quantity):
        with transaction.atomic():
            # check product stock
            shop_product = ShopProduct.objects.get(
                product=product, shop=self.get_shop()
            )

            if quantity > shop_product.stock:
                return

            shop_orderline, created = ShopOrderLine.objects.get_or_create(
                **{
                    "order": self.order,
                    "shop_product": shop_product,
                }
            )

            shop_orderline.quantity = quantity
            shop_orderline.unit_price = Decimal(shop_product.product.retail_price)
            shop_orderline.price = Decimal(shop_product.product.retail_price) * Decimal(
                shop_orderline.quantity
            )
            shop_orderline.save()
            self.update_order()

    def delete_orderline(self, product):
        with transaction.atomic():
            shop_product = ShopProduct.objects.get(
                product=product, shop=self.get_shop()
            )

            shop_orderline = ShopOrderLine.objects.get(
                **{
                    "order": self.order,
                    "shop_product": shop_product,
                }
            )
            shop_orderline.delete()
            self.update_order()

    def add_extraline(self, line_type, quantity, unit_price):
        with transaction.atomic():
            shop_extraline, created = ShopExtraLine.objects.get_or_create(
                **{
                    "order": self.order,
                    "type": line_type,
                }
            )

            if "%" in unit_price:
                shop_extraline.is_percentage = True
                unit_price = unit_price.replace("%", "")
            else:
                shop_extraline.is_percentage = False
            shop_extraline.quantity = quantity
            shop_extraline.unit_price = Decimal(unit_price)
            shop_extraline.price = Decimal(unit_price) * Decimal(quantity)
            shop_extraline.save()
            self.update_order()

    def create_order(self):
        data = {"shop": self.get_shop()}
        self.order = ShopOrder.objects.create(**data)
        return self.order

    def update_order(self):
        data = {"shop": self.get_shop()}
        sub_total = 0
        discount = 0
        tax = 0
        order_lines = ShopOrderLine.objects.filter(order=self.order)

        for order_line in order_lines:
            sub_total += order_line.price

        extra_lines = ShopExtraLine.objects.filter(order=self.order)
        for extra_line in extra_lines:
            if extra_line.type == ShopExtraLineTypes.DISCOUNT:
                if extra_line.is_percentage:
                    discount += (extra_line.price * sub_total) / 100
                else:
                    discount += extra_line.price
            if extra_line.type == ShopExtraLineTypes.TAX:
                if extra_line.is_percentage:
                    tax += (extra_line.price * sub_total) / 100
                else:
                    tax += extra_line.price

        total = (sub_total - discount) + tax
        data.update(
            {
                "sub_total": sub_total,
                "discount": discount,
                "tax": tax,
                "total": total,
            }
        )

        instance = ShopOrder.objects.filter(id=self.order.id).update(**data)
        return instance

    def get_shop(self):
        instance = Shopkeeper.objects.get(employee_id=self.request_user_id)
        return instance.shop

    def active_order_of_shopkeeper(self):
        instance = ShopOrder.objects.filter(
            created_by=self.request_user_id, status=ShopOrderStatus.PENDING
        )

        if instance.exists():
            self.order = instance.first()
            self.order.discount = fix_external_decimal_places(self.order.discount)
            self.order.tax = fix_external_decimal_places(self.order.tax)
        return self.order

    def get_orderlines(self):
        return self.order.orderlines.all().order_by("created_at")

    def get_extralines(self):
        return self.order.extralines.all()

    def get_or_create_order(self):
        if not self.active_order_of_shopkeeper():
            self.create_order()
        return self.order

    def add_lines(self, **kwargs):
        self.get_or_create_order()

        if kwargs.get("product_uuid", None):
            shop_product = ShopProduct.objects.get(
                product__uuid=kwargs["product_uuid"],
                is_active=True,
            )
            self.add_orderline(
                product=shop_product.product,
                quantity=kwargs["quantity"],
            )
        else:
            self.add_extraline(
                line_type=kwargs["type"],
                quantity=kwargs["quantity"],
                unit_price=kwargs["unit_price"],
            )
        return self.order

    def delete_lines(self, **kwargs):
        self.get_or_create_order()

        if kwargs.get("product_uuid", None):
            shop_product = ShopProduct.objects.get(
                product__uuid=kwargs["product_uuid"],
                is_active=True,
            )
            self.delete_orderline(
                product=shop_product.product,
            )
        return self.order

    def complete_order(self):
        if not self.active_order_of_shopkeeper():
            return None
        with transaction.atomic():
            self.order.status = ShopOrderStatus.CONFIRMED
            self.order.save()

            orderlines = self.order.orderlines.all()
            for orderline in orderlines:
                orderline.shop_product.stock = (
                    orderline.shop_product.stock - orderline.quantity
                )
                orderline.status = ShopOrderLineStatus.CONFIRMED
                orderline.shop_product.save()
                orderline.save()

            extralines = self.order.extralines.all()
            for extraline in extralines:
                extraline.status = ShopOrderLineStatus.CONFIRMED
                extraline.save()
        return self.order

    def delete_order(self):
        if not self.active_order_of_shopkeeper():
            return None
        with transaction.atomic():
            if self.order.status == ShopOrderStatus.CONFIRMED:
                return 400
            self.order.orderlines.all().delete()
            self.order.extralines.all().delete()
            self.order.delete()
        return 200

    def get_order(self, id):
        shop = self.get_shop()
        order = ShopOrder.objects.filter(id=id)

        if not order.exists():
            return None
        elif order.first().shop != shop:
            return None

        self.order = order.first()
        self.order.discount = fix_external_decimal_places(self.order.discount)
        self.order.tax = fix_external_decimal_places(self.order.tax)
        return self.order
