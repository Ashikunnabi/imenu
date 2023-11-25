import decimal
from apps.base.service import BaseModelService
from apps.inventory.constants import ProductPriceTypes

from ..models import ProductPrice


class ProductPriceService(BaseModelService):
    model = ProductPrice
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_product_service(self):
        from . import ProductService
        return ProductService()

    def get_product_vat_service(self):
        from . import ProductVatService
        return ProductVatService()

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

        return kwargs, m2m_data

    def create_product_price(self, **kwargs):
        data, m2m_data = self.validated_data(**kwargs)
        return self.create(**data)

    def update_product_price(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        return instance

    def get_prices(self, product_uuid):
        data = {
            "sales_price_in_vat": decimal.Decimal("00.00"),
            "sales_price_ex_vat": decimal.Decimal("00.00"),
            "purchase_price_in_vat": decimal.Decimal("00.00"),
            "purchase_price_ex_vat": decimal.Decimal("00.00"),
        }
        product_prices = self.model.objects.filter(product__uuid=product_uuid)

        for product_price in product_prices:
            price_in_vat = self.get_product_vat_service().get_price_in_vat(
                product_uuid, product_price.price
            )
            price_ex_vat = product_price.price

            if product_price.type == ProductPriceTypes.SALES_PRICE:
                data.update(
                    {
                        "sales_price_in_vat": price_in_vat,
                        "sales_price_ex_vat": price_ex_vat,
                    }
                )
            if product_price.type == ProductPriceTypes.PURCHASE_PRICE:
                data.update(
                    {
                        "purchase_price_in_vat": price_in_vat,
                        "purchase_price_ex_vat": price_ex_vat,
                    }
                )
        return data
