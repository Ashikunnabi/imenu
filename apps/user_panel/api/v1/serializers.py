
from django.conf import settings

from rest_framework import serializers

from apps.user_panel.models import (
    Cart,
    Expense,
    ExpenseType,
    InvoiceOrder,
    Order,
    PurchaseOrder,
    SalesOrder,
    SalesReps,
    FinaleInvoice,
    ManufacturerInvoice,
)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user_json = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    @staticmethod
    def get_user_json(obj):
        return {
            'name': obj.user.name,
            'phone': obj.user.phone
        }


class SalesRepsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesReps
        fields = '__all__'


class FinaleInvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinaleInvoice
        fields = '__all__'


class SalesOrderSerializer(serializers.ModelSerializer):
    is_paid = serializers.SerializerMethodField()

    class Meta:
        model = SalesOrder
        fields = '__all__'

    def get_is_paid(self, obj):
        is_paid = obj.is_paid
        if self.context.get("empty_data"):
            obj.data = {}
        return is_paid


class PurchaseOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class ManufacturerInvoiceSerializer(serializers.ModelSerializer):
    manufacturer_name = serializers.ReadOnlyField(source="manufacturer.name")

    class Meta:
        model = ManufacturerInvoice
        fields = '__all__'


class InvoiceOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceOrder
        fields = '__all__'


class ExpenseTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpenseType
        fields = ['id', 'uuid', 'name', 'is_active', 'created_at']


class ExpenseSerializer(serializers.ModelSerializer):
    spender_human_readable = serializers.CharField(source="spender.name", read_only=True)
    type_human_readable = serializers.CharField(source="type.name", read_only=True)

    class Meta:
        model = Expense
        fields = [
            'uuid',
            'description',
            'value',
            'type',
            'spender',
            'created_at',
            'created_by',
            "spender_human_readable",
            "type_human_readable"
        ]
