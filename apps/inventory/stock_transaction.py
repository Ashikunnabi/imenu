import json
import logging
import string
from django.db import transaction
from apps.inventory.api.v1.serializers import ProductSerializer, StockTransactionSerializer
from datetime import datetime

from apps.inventory.models import (
    Product,
    StockTransaction,
    StockTransactionInWarehouse,
    ProductInwarehouse
)
from apps.user_panel.models import InvoiceOrder, PurchaseOrder, SalesOrder

minimum_selling_price_percentage = 1.4


class Transaction:
    """Calculate/Track/Perform all stock related transactions"""

    def __init__(
        self, 
        transaction_type: float,
        product: Product,
        po: PurchaseOrder,
        so: SalesOrder,
        io: InvoiceOrder,
        discount:float,
        delivery_cost:float,
        notes: string,
        purchase_stock: float,
        purchase_unit_price: float,
        purchase_amount: float,
        sell_stock: float,
        sell_unit_price: float,
        sell_amount: float,
    ) -> None:
        self.transaction_type = transaction_type
        self.product = product
        self.po = po
        self.so = so
        self.io = io
        self.discount = discount
        self.delivery_cost = delivery_cost
        self.notes = notes
        self.purchase_stock = purchase_stock
        self.purchase_unit_price = purchase_unit_price
        self.purchase_amount = purchase_amount
        self.sell_stock = sell_stock
        self.sell_unit_price = sell_unit_price
        self.sell_amount = sell_amount

    def get_last_transaction(self) -> StockTransaction:
        """Get last stock transaction of a product"""

        last_transaction = StockTransaction.objects.filter(product=self.product)

        if last_transaction.exists():
            last_transaction = last_transaction.latest('created_at')
        else:
            last_transaction = StockTransaction(
                product=self.product,
                po=None,
                so=None,
                previous_stock=float(self.product.stock) if self.product.stock not in ['', None] else 0,
                previous_unit_price=(float(self.product.item_price) if self.product.item_price not in ['', None] else 0),
                previous_amount=(
                    (float(self.product.stock) if self.product.stock not in ['', None] else 0)
                    *
                    (float(self.product.item_price) if self.product.item_price not in ['', None] else 0)
                ),
                current_stock=float(self.product.stock) if self.product.stock not in ['', None] else 0,
                current_unit_price=float(self.product.item_price) if self.product.item_price not in ['', None] else 0,
                current_amount=(
                    (float(self.product.stock) if self.product.stock not in ['', None] else 0) 
                    *
                    (float(self.product.item_price) if self.product.item_price not in ['', None] else 0)
                )
            )

        return last_transaction
    
    def calculation(self) -> StockTransaction:
        with transaction.atomic():
            previous_transaction = self.get_last_transaction()
            new_transaction = StockTransaction()
            new_transaction.product = self.product
            new_transaction.po = self.po
            new_transaction.so = self.so
            new_transaction.transaction_type = self.transaction_type
            new_transaction.discount = self.discount
            new_transaction.delivery_cost = self.delivery_cost
            new_transaction.notes = self.notes
            new_transaction.previous_stock = previous_transaction.current_stock
            new_transaction.previous_unit_price = previous_transaction.current_unit_price
            new_transaction.previous_amount = previous_transaction.current_amount

            # TODO: stop processing all input before 2022-04-01
            if self.transaction_type == 1:
                if self.po.date < datetime.strptime('2022-04-01', '%Y-%m-%d').date():
                    return
            if self.transaction_type == 2:
                if self.so.date < datetime.strptime('2022-04-01', '%Y-%m-%d').date():
                    return
            
            if self.transaction_type == 1:
                # purchase transaction
                # calculate purchase stock
                new_transaction.purchase_stock = self.purchase_stock
                new_transaction.purchase_unit_price = self.purchase_unit_price
                new_transaction.purchase_amount = self.purchase_amount
                # calculate current stock
                new_transaction.current_stock = previous_transaction.current_stock + self.purchase_stock
                new_transaction.current_unit_price = (
                    (previous_transaction.current_amount + self.purchase_amount) 
                    / 
                    (previous_transaction.current_stock + self.purchase_stock)
                )
                new_transaction.current_amount = previous_transaction.current_amount + self.purchase_amount
            elif self.transaction_type == 2:
                # sell transaction
                # calculate sell stock
                new_transaction.sell_stock = self.sell_stock
                new_transaction.sell_unit_price = self.sell_unit_price
                new_transaction.sell_amount = self.sell_amount
                # calculate current stock
                new_transaction.current_stock = previous_transaction.current_stock - self.sell_stock
                new_transaction.current_unit_price = previous_transaction.current_unit_price
                new_transaction.current_amount = previous_transaction.current_amount - (
                    self.sell_stock
                    *
                    previous_transaction.current_unit_price
                )
                # calculate sell with profit stock 
                new_transaction.sell_unit_price_profit = self.sell_unit_price - previous_transaction.current_unit_price
                new_transaction.sell_amount_profit = new_transaction.sell_unit_price_profit * self.sell_stock
            new_transaction.save()

            # update product 
            self.product.stock=int(new_transaction.current_stock)
            self.product.average_cost=new_transaction.current_unit_price
            self.product.item_price=new_transaction.current_unit_price * minimum_selling_price_percentage
            self.product.save()
            
            logging.getLogger('warning_logger').warning('PRODUCT')
            logging.getLogger('warning_logger').warning(ProductSerializer(self.product).data)

            logging.getLogger('warning_logger').warning('STOCK TRANSACTION')
            logging.getLogger('warning_logger').warning(StockTransactionSerializer(new_transaction).data)
