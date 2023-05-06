from django.db import models

from apps.core.rbac.models import BaseModel
class StockTransaction(BaseModel):
    from apps.main.user_panel.models import InvoiceOrder, PurchaseOrder, SalesOrder

    TRANSACTION_TYPE = (
        (1, "Purchase"),
        (2, "Sell"),
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    po = models.ForeignKey(
        PurchaseOrder, on_delete=models.PROTECT, blank=True, null=True
    )
    so = models.ForeignKey(SalesOrder, on_delete=models.PROTECT, blank=True, null=True)
    invoice = models.ForeignKey(
        InvoiceOrder, on_delete=models.PROTECT, blank=True, null=True
    )
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE)

    # opening stock
    previous_stock = models.FloatField(default=0)
    previous_unit_price = models.FloatField(default=0)
    previous_amount = models.FloatField(default=0)

    # purchase stock details
    purchase_stock = models.FloatField(default=0)
    purchase_unit_price = models.FloatField(default=0)
    purchase_amount = models.FloatField(default=0)

    sell_stock = models.FloatField(default=0)
    # selling stock details without profit (genuanine)
    sell_unit_price = models.FloatField(default=0)
    sell_amount = models.FloatField(default=0)
    # selling stock details with profit
    sell_unit_price_profit = models.FloatField(default=0)
    sell_amount_profit = models.FloatField(default=0)

    # after purchase/sell current stock
    current_stock = models.FloatField(default=0)
    current_unit_price = models.FloatField(default=0)
    current_amount = models.FloatField(default=0)

    discount = models.FloatField(default=0)
    delivery_cost = models.FloatField(default=0)
    notes = models.TextField(default="")

    def __str__(self):
        return f"{self.product.product_id} at {self.transaction_type}"


class StockTransactionInWarehouse(BaseModel):
    stock_transaction = models.ForeignKey(StockTransaction, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(warehouse, on_delete=models.PROTECT)
    stock = models.FloatField(default=0)

    def __str__(self):
        return f"{self.stock_transaction.id} at {self.warehouse.name}"
