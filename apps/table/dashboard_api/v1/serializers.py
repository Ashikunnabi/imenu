from apps.inventory.api.v1.serializers import DocumentOutputSerializer
from rest_framework import serializers

from apps.base.utils.basic import build_media_url

from ...models import Table, TableType, TableCode, TableDocument


class TableTypeInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = [
            "name",
            "is_active",
        ]


class TableTypeOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = [
            "uuid",
            "name",
            "is_active",
        ]


class TableInputSerializer(serializers.ModelSerializer):
    type_uuid = serializers.UUIDField()

    class Meta:
        model = Table
        fields = [
            "name",
            "type_uuid",
            "start_at",
            "end_at",
            "is_active",
        ]


class TableOutputSerializer(serializers.ModelSerializer):
    type = TableTypeOutputSerializer()

    class Meta:
        model = Table
        fields = [
            "uuid",
            "name",
            "type",
            "start_at",
            "end_at",
            "is_active",
        ]


class TableCodeInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableCode
        fields = [
            "type",
            "value",
        ]


class TableCodeOutputSerializer(serializers.ModelSerializer):
    qr_code_path = serializers.CharField()

    class Meta:
        model = TableCode
        fields = [
            "uuid",
            "type",
            "value",
            "qr_code_path",
        ]


class TableDocumentInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableDocument
        fields = "__all__"


class TableDocumentOutputSerializer(serializers.ModelSerializer):
    document = DocumentOutputSerializer()

    class Meta:
        model = TableDocument
        fields = [
            "uuid",
            "type",
            "document",
            "sort_order",
        ]


class TableCodeQRCodeGenerateInputSerializer(serializers.Serializer):
    data = serializers.CharField()


class TableCodeQRCodeGenerateOutputSerializer(serializers.Serializer):
    path = serializers.CharField()


class TableDocumentUploadInputSerializer(serializers.Serializer):
    file = serializers.FileField()
    sort_order = serializers.IntegerField()
