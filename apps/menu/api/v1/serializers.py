from apps.inventory.api.v1.serializers import ProductOutputSerializer
from rest_framework import serializers

from apps.base.utils.basic import build_media_url

from ...models import Menu, MenuType, MenuItem


class MenuTypeInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuType
        fields = [
            "name",
            "is_active",
        ]


class MenuTypeOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuType
        fields = [
            "uuid",
            "name",
            "is_active",
        ]


class MenuInputSerializer(serializers.ModelSerializer):
    type_uuid = serializers.UUIDField()

    class Meta:
        model = Menu
        fields = [
            "name",
            "type_uuid",
            "start_at",
            "end_at",
            "is_active",
        ]


class MenuOutputSerializer(serializers.ModelSerializer):
    type = MenuTypeOutputSerializer()

    class Meta:
        model = Menu
        fields = [
            "uuid",
            "name",
            "type",
            "start_at",
            "end_at",
            "is_active",
        ]


class MenuItemInputSerializer(serializers.ModelSerializer):
    menu_uuid = serializers.UUIDField()
    item_uuid = serializers.UUIDField()

    class Meta:
        model = MenuItem
        fields = [
            "menu_uuid",
            "item_uuid",
            "start_at",
            "end_at",
        ]


class MenuItemOutputSerializer(serializers.ModelSerializer):
    menu = MenuOutputSerializer()
    item = ProductOutputSerializer()

    class Meta:
        model = MenuItem
        fields = [
            "uuid",
            "menu",
            "item",
            "start_at",
            "end_at",
            "is_active",
        ]
