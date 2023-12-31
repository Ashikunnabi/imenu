import decimal
from apps.base.service import BaseModelService
from apps.inventory.services.product_service import ProductService
from apps.inventory.services.vat_service import VatService

from ..models import ProductVat


class ProductVatService(BaseModelService):
    model = ProductVat
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_product_service(self):
        return ProductService()

    def get_vat_service(self):
        return VatService()

    def validated_data(self, **kwargs):
        m2m_data = {}
        m2m_keys = ["permissions", "users"]

        for m2m_key in m2m_keys:
            if m2m_key in kwargs:
                m2m_data[m2m_key] = kwargs.pop(m2m_key)

        if "product_uuid" in kwargs:
            product = self.get_product_service().read_by_uuid(
                uuid_value=kwargs.pop("product_uuid")
            )
            kwargs["product_id"] = product.id

        if "vat_uuid" in kwargs:
            vat = self.get_vat_service().read_by_uuid(uuid_value=kwargs.pop("vat_uuid"))
            kwargs["vat_id"] = vat.id
        return kwargs, m2m_data

    def create_product_vat(self, **kwargs):
        data, m2m_data = self.validated_data(**kwargs)

        # check object already exists
        self.does_object_already_exists(**data)
        return self.create(**data)

    def update_product_vat(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance

    def default_vat(self):
        return decimal.Decimal("1") + decimal.Decimal("00.00")

    def default_vat_type(self):
        return "percentage"

    def get_vat(self, product_uuid):
        vat = self.default_vat()
        vat_type = self.default_vat_type()

        product_vat = self.model.objects.filter(
            product__uuid=product_uuid,
            vat__is_active=True,
            is_active=True,
        ).last()

        if product_vat:
            if product_vat.flat:
                vat = product_vat.flat
                vat_type = "flat"
            else:
                vat = decimal.Decimal("1") + (
                    product_vat.percentage / decimal.Decimal("100")
                )

        return vat, vat_type

    def get_price_in_vat(self, product_uuid, price_ex_vat):
        vat, vat_type = self.get_vat(product_uuid=product_uuid)
        price = price_ex_vat
        print(vat)

        if vat_type == "percentage":
            price = decimal.Decimal(str(price_ex_vat)) * vat
        else:
            price = decimal.Decimal(str(price_ex_vat)) + decimal.Decimal(str(vat))

        return price

    def get_price_ex_vat(self, product_uuid, price_in_vat):
        vat, vat_type = self.get_vat(product_uuid=product_uuid)
        price = price_in_vat

        if vat_type == "percentage":
            price = decimal.Decimal(str(price_in_vat)) / vat
        else:
            price = decimal.Decimal(str(price_in_vat)) - decimal.Decimal(str(vat))

        return price
