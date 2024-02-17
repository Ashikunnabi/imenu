from apps.order.constants import OrderStatus
from apps.table.dashboard_api.v1.serializers import TableOutputSerializer
from rest_framework import serializers

from apps.inventory.api.v1.serializers import ProductOutputSerializer

from ...models import Order, OrderLine


class DashboardOrderLineOutputSerializer(serializers.ModelSerializer):
    product = ProductOutputSerializer()
    price_ex_vat = serializers.DecimalField(max_digits=18, decimal_places=2)
    price_in_vat = serializers.DecimalField(max_digits=18, decimal_places=2)
    total_price_ex_vat = serializers.DecimalField(max_digits=18, decimal_places=2)
    total_price_in_vat = serializers.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        model = OrderLine
        fields = "__all__"


class DashboardOrderInputSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=OrderStatus.CHOICES)


class DashboardOrderOutputSerializer(serializers.ModelSerializer):
    lines = DashboardOrderLineOutputSerializer(many=True)
    total_price_ex_vat = serializers.DecimalField(max_digits=18, decimal_places=2)
    total_price_in_vat = serializers.DecimalField(max_digits=18, decimal_places=2)
    vat = serializers.DecimalField(max_digits=18, decimal_places=2)
    table = TableOutputSerializer()

    class Meta:
        model = Order
        fields = "__all__"
