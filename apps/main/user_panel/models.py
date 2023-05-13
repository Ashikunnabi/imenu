# from django.db import models
# from django.contrib.auth import get_user_model

# from apps.core.rbac.models import BaseModel
# from apps.main.inventory.models import Brand, Product

# User = get_user_model()


# class Cart(BaseModel):
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     # product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True,
#     #                             null=True)
#     product_json = models.JSONField(blank=False, null=False)
#     quantity = models.CharField(max_length=256, blank=False, null=False)
#     unit_price = models.CharField(max_length=256, blank=False, null=False)
#     total_price = models.CharField(max_length=256, blank=True, null=True)
#     discount = models.CharField(max_length=256, blank=True, null=True)
#     is_ordered = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.name


# class Order(BaseModel):
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     carts = models.ManyToManyField(Cart)
#     carts_json = models.JSONField(blank=False, null=False)
#     total_price = models.CharField(max_length=256, blank=False, null=False)
#     po_number = models.CharField(max_length=256)
#     billing_full_name = models.CharField(max_length=256)
#     billing_address = models.TextField(default='')
#     billing_city = models.CharField(max_length=256)
#     billing_state = models.CharField(max_length=256)  # {value: '', text: ''}
#     billing_postal_code = models.CharField(max_length=256)
#     billing_phone = models.CharField(max_length=256)
#     billing_email = models.CharField(max_length=256, blank=True, null=True)
#     shipping_full_name = models.CharField(max_length=256)
#     delivery_address = models.TextField(default='')
#     shipping_city = models.CharField(max_length=256)
#     shipping_state = models.CharField(max_length=256)  # {value: '', text: ''}
#     shipping_postal_code = models.CharField(max_length=256)
#     shipping_phone = models.CharField(max_length=256)
#     shipping_email = models.CharField(max_length=256, blank=True, null=True)
#     transaction_code = models.CharField(max_length=256)
#     transaction_response = models.JSONField()
#     is_ordered = models.BooleanField(default=False)
#     is_cancelled = models.BooleanField(default=False)
#     in_processing = models.BooleanField(default=False)
#     is_delivered = models.BooleanField(default=False)
#     tracking_number = models.CharField(max_length=265, blank=True, null=True)
#     tracking_number_added_at = models.DateField(blank=True, null=True)
#     invoice = models.CharField(max_length=256, blank=True, null=True)

#     # def __str__(self):
#     #     return self.user.name

#     def created_date(self):
#         return self.created_at.strftime('%B %d, %Y')


# class SalesReps(BaseModel):
#     name = models.CharField(max_length=256)
#     title = models.CharField(max_length=256, blank=True, null=True)
#     email = models.EmailField(max_length=256)
#     phone = models.CharField(max_length=256)
#     image = models.CharField(max_length=256, blank=True, null=True)

#     def __str__(self):
#         return self.name


# class DealerSalesReps(BaseModel):
#     dealer = models.ForeignKey(User, on_delete=models.CASCADE)
#     sales_reps = models.ManyToManyField(SalesReps, blank=True)

#     def __str__(self):
#         return self.dealer.name


# class FinaleInvoice(BaseModel):
#     dealer = models.ForeignKey(User, on_delete=models.CASCADE)
#     invoice = models.CharField(max_length=256)
#     tracking_number = models.CharField(max_length=265, blank=True, null=True)
#     tracking_number_added_at = models.DateField(blank=True, null=True)

#     def __str__(self):
#         return self.dealer.name


# class InvoiceOrder(BaseModel):
#     number = models.CharField(max_length=256)
#     date = models.DateField(blank=True, null=True)
#     data = models.JSONField(blank=True, null=True)
#     is_stock_updated = models.BooleanField(default=False)
#     is_locked = models.BooleanField(default=False)

#     def __str__(self):
#         return self.number


# class SalesOrder(BaseModel):
#     number = models.CharField(max_length=256)
#     date = models.DateField(blank=True, null=True)
#     due_date = models.DateField(blank=True, null=True)
#     data = models.JSONField(blank=True, null=True)
#     is_stock_updated = models.BooleanField(default=False)
#     is_locked = models.BooleanField(default=False)
#     is_quotation = models.BooleanField(default=False)
#     is_dropship = models.BooleanField(default=False)
#     is_ready_for_processing = models.BooleanField(default=False)
#     notes = models.TextField(blank=True, default="")
#     invoice_number = models.CharField(max_length=265, blank=True, default="")
#     ship_via = models.CharField(max_length=265, blank=True, default="")
#     tracking_number = models.CharField(max_length=265, blank=True, default="")
#     freight = models.CharField(max_length=265, blank=True, default="")
#     customer_note = models.TextField(blank=True, default="")

#     def __str__(self):
#         return self.number
    
#     @property
#     def is_paid(self):
#         is_paid = True
#         products = self.data.get("products")

#         for product in products:
#             if product.get("pending") not in ["", "0", 0]:
#                 is_paid = False
#                 break
#         return is_paid


# class PurchaseOrder(BaseModel):
#     number = models.CharField(max_length=256)
#     date = models.DateField(blank=True, null=True)
#     due_date = models.DateField(blank=True, null=True)
#     data = models.JSONField(blank=True, null=True)
#     is_stock_updated = models.BooleanField(default=False)
#     is_locked = models.BooleanField(default=False)
#     is_ready_for_processing = models.BooleanField(default=False)
#     notes = models.TextField(blank=True, default="")
#     customer_note = models.TextField(blank=True, default="")

#     def __str__(self):
#         return self.number


# class ManufacturerInvoice(BaseModel):
#     # manufacturer = models.ForeignKey(Brand, on_delete=models.CASCADE)
#     invoice = models.CharField(max_length=256)
#     distributor = models.CharField(max_length=265, blank=True, null=True)

#     def __str__(self):
#         return self.dealer.name


# class ExpenseType(BaseModel):
#     name = models.CharField(max_length=256)

#     def __str__(self):
#         return self.name


# class Expense(BaseModel):
#     description = models.CharField(max_length=256)
#     value = models.FloatField(default=0)
#     type = models.ForeignKey(ExpenseType, on_delete=models.PROTECT, related_name="expenses")
#     spender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="expenses", null=True)

#     def __str__(self):
#         return self.description
