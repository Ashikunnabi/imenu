from rest_framework import serializers

from ...models import Order


class OrderSerializer(serializers.ModelSerializer):
    user_json = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    @staticmethod
    def get_user_json(obj):
        return {"name": obj.user.name, "phone": obj.user.phone}
