from apps.table.dashboard_api.v1.serializers import TableOutputSerializer
from rest_framework import serializers

from apps.inventory.api.v1.serializers import ProductOutputSerializer

from ...models import Order, OrderLine


class OrderLineOutputSerializer(serializers.ModelSerializer):
    product = ProductOutputSerializer()
    price_ex_vat = serializers.DecimalField(max_digits=18, decimal_places=2)
    price_in_vat = serializers.DecimalField(max_digits=18, decimal_places=2)
    total_price_ex_vat = serializers.DecimalField(max_digits=18, decimal_places=2)
    total_price_in_vat = serializers.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        model = OrderLine
        fields = "__all__"


class OrderInputSerializer(serializers.Serializer):
    cart_uuid = serializers.UUIDField()


class OrderOutputSerializer(serializers.ModelSerializer):
    lines = OrderLineOutputSerializer(many=True)
    total_price_ex_vat = serializers.DecimalField(max_digits=18, decimal_places=2)
    total_price_in_vat = serializers.DecimalField(max_digits=18, decimal_places=2)
    vat = serializers.DecimalField(max_digits=18, decimal_places=2)
    table = TableOutputSerializer()

    class Meta:
        model = Order
        fields = "__all__"
