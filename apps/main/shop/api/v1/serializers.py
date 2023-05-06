from apps.main.inventory.models import Product
from rest_framework import serializers

from ...models import (
    Shop,
    ShopExtraLine,
    ShopOrder,
    ShopOrderLine,
    Shopkeeper,
    ShopProduct,
)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


class ShopkeeperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopkeeper
        fields = "__all__"


class ShopProductSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    is_shop_product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_stock(self, obj):
        stock = 0
        product = ShopProduct.objects.filter(product=obj)
        if product.exists():
            stock = product.first().stock
        return stock

    def get_is_active(self, obj):
        is_active = False
        product = ShopProduct.objects.filter(product=obj)
        if product.exists():
            is_active = product.first().is_active
        return is_active

    def get_is_shop_product(self, obj):
        is_shop_product = False
        product = ShopProduct.objects.filter(product=obj)
        if product.exists():
            is_shop_product = True
        return is_shop_product


class ShopProductInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopProduct
        fields = "__all__"


class ShopOrderLineSerializer(serializers.ModelSerializer):
    product_uuid = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
    unit_price = serializers.DecimalField(max_digits=15, decimal_places=2)
    price = serializers.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        model = ShopOrderLine
        fields = "__all__"

    def get_product_uuid(self, obj):
        return obj.shop_product.product.uuid

    def get_product_id(self, obj):
        return obj.shop_product.product.product_id


class ShopExtraLineSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        model = ShopExtraLine
        fields = "__all__"


class ShopOrderSerializer(serializers.ModelSerializer):
    order_lines = ShopOrderLineSerializer(many=True, allow_null=True)
    extra_lines = ShopExtraLineSerializer(many=True, allow_null=True)
    sub_total = serializers.DecimalField(max_digits=15, decimal_places=2)
    discount = serializers.CharField()
    tax = serializers.CharField()
    total = serializers.DecimalField(max_digits=15, decimal_places=2)
    shop = ShopSerializer()

    class Meta:
        model = ShopOrder
        fields = "__all__"
