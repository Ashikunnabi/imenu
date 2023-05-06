from django.db import models
from django.contrib.auth import get_user_model

from apps.core.rbac.models import BaseModel
from apps.main.inventory.models import Product

User = get_user_model()


class ShopOrderStatus:
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    REFUND = "refund"

    CHOICES = (
        (PENDING, "PENDING"),
        (CONFIRMED, "CONFIRMED"),
        (CANCELED, "CANCELED"),
        (REFUND, "REFUND"),
    )


class ShopOrderLineStatus:
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    REFUND = "refund"

    CHOICES = (
        (PENDING, "PENDING"),
        (CONFIRMED, "CONFIRMED"),
        (CANCELED, "CANCELED"),
        (REFUND, "REFUND"),
    )


class ShopExtraLineTypes:
    DISCOUNT = "discount"
    TAX = "tax"

    CHOICES = (
        (DISCOUNT, "DISCOUNT"),
        (TAX, "TAX"),
    )


class Shop(BaseModel):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=256, blank=True, null=True)
    phone_numbers = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "location"],
                name="unique_shop_name_location",
            )
        ]

    def __str__(self):
        return self.name


class Shopkeeper(BaseModel):
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shopkeepers"
    )
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shopkeepers")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "shop"],
                name="unique_shopkeeper_employee_shop",
            )
        ]

    def __str__(self):
        return self.name


class ShopProduct(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="shop_products"
    )
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="shop_products"
    )
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "shop"],
                name="unique_shopproduct_product_shop",
            )
        ]


class ShopOrder(BaseModel):
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT, related_name="orders")
    sub_total = models.DecimalField(default="00.00", max_digits=15, decimal_places=6)
    discount = models.DecimalField(default="00.00", max_digits=15, decimal_places=6)
    tax = models.DecimalField(default="00.00", max_digits=15, decimal_places=6)
    total = models.DecimalField(default="00.00", max_digits=15, decimal_places=6)
    status = models.CharField(
        choices=ShopOrderStatus.CHOICES, default=ShopOrderStatus.PENDING, max_length=256
    )


class ShopOrderLine(BaseModel):
    order = models.ForeignKey(
        ShopOrder, on_delete=models.PROTECT, related_name="orderlines"
    )
    shop_product = models.ForeignKey(
        ShopProduct, on_delete=models.PROTECT, related_name="orderlines"
    )
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(default="00.00", max_digits=15, decimal_places=6)
    price = models.DecimalField(default="00.00", max_digits=15, decimal_places=6)
    status = models.CharField(
        choices=ShopOrderLineStatus.CHOICES,
        default=ShopOrderLineStatus.PENDING,
        max_length=256,
    )


class ShopExtraLine(BaseModel):
    order = models.ForeignKey(
        ShopOrder, on_delete=models.PROTECT, related_name="extralines"
    )
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(default="00.00", max_digits=15, decimal_places=6)
    price = models.DecimalField(default="00.00", max_digits=15, decimal_places=6)
    type = models.CharField(
        choices=ShopExtraLineTypes.CHOICES,
        default=ShopExtraLineTypes.TAX,
        max_length=256,
    )
    status = models.CharField(
        choices=ShopOrderLineStatus.CHOICES,
        default=ShopOrderLineStatus.PENDING,
        max_length=256,
    )
    is_percentage = models.BooleanField(default=False)
