from itertools import chain

from django.core.management.base import BaseCommand, CommandError

from apps.inventory.models import Product
from apps.user_panel.models import PurchaseOrder, SalesOrder


class Command(BaseCommand):
    help = "Update product details of PO/SO"

    def update_details(self, po_so_product_data):
        try:
            product = Product.objects.get(id=po_so_product_data["id"])
        except Exception as ex:
            self.stdout.write(
                self.style.ERROR(
                    'FAILED: Product ("%s") not found' % po_so_product_data["id"]
                )
            )
            raise ex
        
        data = {
            "uuid": product.uuid,
            "product_id": product.product_id
        }

        po_so_product_data.update(data)
        return po_so_product_data

    def handle(self, *args, **options):
        for data in list(chain(SalesOrder.objects.all(), PurchaseOrder.objects.all())):
            for index, product in enumerate(data.data["products"]):
                data.data["products"][index] = self.update_details(product)
            data.save()
            self.stdout.write(
                self.style.SUCCESS(
                    'Updated: "%s"' % data.number
                )
            )
        self.stdout.write(
            self.style.SUCCESS(
                'END'
            )
        )
                
