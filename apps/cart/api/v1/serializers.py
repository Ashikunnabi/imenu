from rest_framework import serializers


from ...models import Cart, CartLine


class CartLineInputSerializer(serializers.Serializer):
    product_uuids = serializers.UUIDField()
    quantity = serializers.IntegerField()


class CartLineOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartLine


class CartInputSerializer(serializers.Serializer):
    lines = CartLineInputSerializer(many=True)


class CartOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
