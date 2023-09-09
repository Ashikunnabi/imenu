from apps.inventory.api.v1.serializers import ProductOutputSerializer
from rest_framework import serializers


from ...models import Cart, CartLine


class CartLineInputSerializer(serializers.Serializer):
    product_uuid = serializers.UUIDField(required=False)
    quantity = serializers.IntegerField()


class CartLineOutputSerializer(serializers.ModelSerializer):
    product = ProductOutputSerializer()
    price_ex_vat = serializers.DecimalField(max_digits=6, decimal_places=2)
    price_in_vat = serializers.DecimalField(max_digits=6, decimal_places=2)
    total_price_ex_vat = serializers.DecimalField(max_digits=6, decimal_places=2)
    total_price_in_vat = serializers.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        model = CartLine
        fields = "__all__"


class CartInputSerializer(serializers.Serializer):
    table_uuid = serializers.UUIDField()
    lines = CartLineInputSerializer(many=True)


class CartOutputSerializer(serializers.ModelSerializer):
    lines = CartLineOutputSerializer(many=True)
    total_price_ex_vat = serializers.DecimalField(max_digits=6, decimal_places=2)
    total_price_in_vat = serializers.DecimalField(max_digits=6, decimal_places=2)
    vat = serializers.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        model = Cart
        fields = "__all__"
