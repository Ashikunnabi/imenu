from rest_framework import serializers

from apps.base.utils.basic import build_media_url

from ...models import (
    Attribute,
    AttributeGroup,
    Brand,
    Document,
    Group,
    Product,
    ProductAttribute,
    ProductCode,
    ProductDocument,
    ProductPrice,
    ProductUnit,
    ProductVat,
    ProductWarehouse,
    Supplier,
    Type,
    Warehouse,
    Unit,
    Vat,
)


class AttributeGroupInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeGroup
        fields = [
            "name",
            "is_active",
        ]


class AttributeGroupOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeGroup
        fields = [
            "uuid",
            "name",
            "is_active",
        ]


class AttributeInputSerializer(serializers.ModelSerializer):
    attribute_group_uuid = serializers.UUIDField()

    class Meta:
        model = Attribute
        fields = [
            "name",
            "attribute_group_uuid",
            "is_active",
        ]


class AttributeOutputSerializer(serializers.ModelSerializer):
    attribute_group = AttributeGroupOutputSerializer()

    class Meta:
        model = Attribute
        fields = [
            "uuid",
            "attribute_group",
            "name",
            "is_active",
        ]


class BrandInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class BrandOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            "uuid",
            "address",
            "email",
            "name",
            "phone",
            "tagline",
            "url",
        ]


class DocumentInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class DocumentOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = [
            "uuid",
            "extension",
            "is_encrypted",
            "is_active",
            "name",
            "file",
        ]


class GroupInputSerializer(serializers.ModelSerializer):
    parent_uuid = serializers.UUIDField(required=False)

    class Meta:
        model = Group
        fields = [
            "code",
            "name",
            "parent_uuid",
            "is_active",
        ]


class GroupOutputSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            "uuid",
            "code",
            "name",
            "parent",
            "is_active",
        ]

    def get_parent(self, obj):
        if not obj.parent:
            return None
        return self.__class__(obj.parent).data


class ProductAttributeInputSerializer(serializers.ModelSerializer):
    attribute_uuid = serializers.UUIDField(required=False)
    attribute_group_uuid = serializers.UUIDField()
    name = serializers.CharField(required=False)
    value = serializers.CharField()

    class Meta:
        model = ProductAttribute
        fields = [
            "attribute_uuid",
            "attribute_group_uuid",
            "name",
            "value",
        ]

    def validate(self, data):
        if not data.get("attribute_uuid", None) and not data.get("name", None):
            raise serializers.ValidationError(
                "Attribute uuid/name at least 1 is required"
            )
        if data.get("attribute_uuid", None) and data.get("name", None):
            raise serializers.ValidationError("Attribute uuid/name only 1 is required")
        return data


class ProductAttributeOutputSerializer(serializers.ModelSerializer):
    attribute = AttributeOutputSerializer()

    class Meta:
        model = ProductAttribute
        fields = [
            "attribute",
            "value",
        ]


class ProductCodeInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCode
        fields = [
            "type",
            "value",
        ]


class ProductCodeOutputSerializer(serializers.ModelSerializer):
    qr_code_path = serializers.CharField()

    class Meta:
        model = ProductCode
        fields = [
            "uuid",
            "type",
            "value",
            "qr_code_path",
        ]


class ProductDocumentInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDocument
        fields = "__all__"


class ProductDocumentOutputSerializer(serializers.ModelSerializer):
    document = DocumentOutputSerializer()

    class Meta:
        model = ProductDocument
        fields = [
            "uuid",
            "type",
            "sort_order",
            "document",
        ]


class ProductPriceInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = [
            "type",
            "price",
        ]


class ProductPriceOutputSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        model = ProductPrice
        fields = [
            "uuid",
            "type",
            "price",
        ]


class SupplierInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class SupplierOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class TypeInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class TypeOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class WarehouseInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"


class WarehouseOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"


class ProductWarehouseInputSerializer(serializers.ModelSerializer):
    product_uuid = serializers.UUIDField()
    warehouse_uuid = serializers.UUIDField()

    class Meta:
        model = ProductWarehouse
        fields = [
            "product_uuid",
            "warehouse_uuid",
            "stock",
        ]


class ProductWarehouseOutputSerializer(serializers.ModelSerializer):
    warehouse = WarehouseOutputSerializer()
    stock = serializers.DecimalField(decimal_places=2, max_digits=18)

    class Meta:
        model = ProductWarehouse
        fields = [
            "uuid",
            "warehouse",
            "stock",
        ]


class ProductQRCodeGenerateInputSerializer(serializers.Serializer):
    data = serializers.CharField()


class ProductQRCodeGenerateOutputSerializer(serializers.Serializer):
    path = serializers.CharField()


class ProductCodeQRCodeGenerateInputSerializer(serializers.Serializer):
    data = serializers.CharField()


class ProductCodeQRCodeGenerateOutputSerializer(serializers.Serializer):
    path = serializers.CharField()


class UnitInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = [
            "code",
            "name",
            "is_active",
        ]


class UnitOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = [
            "uuid",
            "name",
            "code",
            "is_active",
        ]


class VatInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vat
        fields = [
            "code",
            "name",
            "is_active",
        ]


class VatOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vat
        fields = [
            "uuid",
            "code",
            "name",
            "is_active",
        ]


class ProductUnitInputSerializer(serializers.ModelSerializer):
    unit_uuid = serializers.UUIDField()

    class Meta:
        model = ProductUnit
        fields = [
            "unit_uuid",
            "min",
            "max",
        ]


class ProductUnitOutputSerializer(serializers.ModelSerializer):
    min = serializers.DecimalField(decimal_places=2, max_digits=18)
    max = serializers.DecimalField(decimal_places=2, max_digits=18)
    unit = UnitOutputSerializer()

    class Meta:
        model = ProductUnit
        fields = [
            "uuid",
            "unit",
            "min",
            "max",
        ]


class ProductVatInputSerializer(serializers.ModelSerializer):
    vat_uuid = serializers.UUIDField()

    class Meta:
        model = ProductVat
        fields = [
            "vat_uuid",
            "flat",
            "percentage",
        ]


class ProductVatOutputSerializer(serializers.ModelSerializer):
    flat = serializers.DecimalField(decimal_places=2, max_digits=18)
    percentage = serializers.DecimalField(decimal_places=2, max_digits=18)
    vat = VatOutputSerializer()

    class Meta:
        model = ProductVat
        fields = [
            "uuid",
            "vat",
            "flat",
            "percentage",
        ]


class ProductInputSerializer(serializers.ModelSerializer):
    parent_uuid = serializers.UUIDField(required=False)
    brand_uuid = serializers.UUIDField()
    group_uuid = serializers.UUIDField()
    type_uuid = serializers.UUIDField()

    class Meta:
        model = Product
        fields = [
            "code",
            "name",
            "description",
            "short_description",
            "family",
            "series",
            "parent_uuid",
            "brand_uuid",
            "group_uuid",
            "type_uuid",
            "is_active",
        ]


class ProductOutputSerializer(serializers.ModelSerializer):
    qr_code_path = serializers.CharField(allow_null=True)
    brand = BrandOutputSerializer()
    group = GroupOutputSerializer()
    parent = serializers.SerializerMethodField()
    type = TypeOutputSerializer()

    class Meta:
        model = Product
        fields = [
            "brand",
            "code",
            "description",
            "family",
            "group",
            "is_active",
            "name",
            "parent",
            "series",
            "short_description",
            "type",
            "uuid",
            "qr_code_path",
        ]

    def get_parent(self, obj):
        if obj.parent:
            return self.__class__(obj.parent).data

class ProductSearchOutputSerializer(serializers.Serializer):
    brand = BrandOutputSerializer()
    group = GroupOutputSerializer()
    parent = serializers.DictField()
    type = TypeOutputSerializer()
    uuid = serializers.UUIDField()
    code = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    short_description = serializers.CharField()
    family = serializers.CharField()
    series = serializers.CharField()
    is_active = serializers.BooleanField()
    documents = ProductDocumentOutputSerializer(many=True)
    prices = ProductPriceOutputSerializer(many=True)


class ProductDocumentUploadInputSerializer(serializers.Serializer):
    file = serializers.FileField()
    sort_order = serializers.IntegerField()
