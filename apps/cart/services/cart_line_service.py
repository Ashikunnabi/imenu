import decimal
from apps.base.service import BaseModelService
from apps.base.utils.basic import fix_internal_decimal_places
from apps.inventory.services import ProductService, ProductPriceService

from ..models import CartLine


class CartLineService(BaseModelService):
    model = CartLine
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_service = self.get_product_service()

    def get_product_service(self):
        return ProductService()

    def get_product_price_service(self):
        return ProductPriceService()

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

        # Default price
        kwargs["price_in_vat"] = decimal.Decimal("00.00")
        kwargs["price_ex_vat"] = decimal.Decimal("00.00")
        kwargs["total_price_in_vat"] = decimal.Decimal("00.00")
        kwargs["total_price_ex_vat"] = decimal.Decimal("00.00")
        return kwargs, m2m_data

    def create_cart_line(self, **kwargs):
        data, m2m_data = self.validated_data(**kwargs)

        # check object already exists
        self.does_object_already_exists(**data)

        cart_line = self.create(**data)
        self.calculate_price(line=cart_line)
        return cart_line

    def update_cart_line(self, instance, **kwargs):
        kwargs, m2m_data = self.validated_data(**kwargs)
        instance = self.update_model_instance(instance, **kwargs)
        self.calculate_price(line=instance)
        return instance

    def get_actual_product_price(self, product_uuid):
        return self.get_product_price_service().get_prices(product_uuid=product_uuid)

    def get_actual_product_sales_prices(self, product_uuid):
        price_in_vat = self.get_actual_product_price(product_uuid=product_uuid)[
            "sales_price_in_vat"
        ]
        price_ex_vat = self.get_actual_product_price(product_uuid=product_uuid)[
            "sales_price_ex_vat"
        ]
        return price_in_vat, price_ex_vat

    def get_actual_product_purchase_prices(self, product_uuid):
        price_in_vat = self.get_actual_product_price(product_uuid=product_uuid)[
            "purchase_price_in_vat"
        ]
        price_ex_vat = self.get_actual_product_price(product_uuid=product_uuid)[
            "purchase_price_ex_vat"
        ]
        return price_in_vat, price_ex_vat

    def calculate_price(self, line):
        price_in_vat, price_ex_vat = self.get_actual_product_sales_prices(
            product_uuid=line.product.uuid
        )
        line.price_in_vat = fix_internal_decimal_places(price_in_vat)
        line.price_ex_vat = fix_internal_decimal_places(price_ex_vat)
        line.total_price_ex_vat = fix_internal_decimal_places(
            decimal.Decimal(line.quantity) * line.price_ex_vat
        )
        line.total_price_in_vat = fix_internal_decimal_places(
            decimal.Decimal(line.quantity) * line.price_in_vat
        )
        line.save()
        return line
