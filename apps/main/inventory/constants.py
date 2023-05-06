class ProductPriceTypes:
    PURCHASE_PRICE = "purchase_price"
    SALES_PRICE = "sales_price"

    CHOICES = (
        (PURCHASE_PRICE, "Purchase Price"),
        (SALES_PRICE, "Sales Price"),
    )


class ProductCodeTypes:
    IAN = "ian"
    UPC = "upc"
    MANUFACTURE = "manufacture"

    CHOICES = (
        (IAN, "IAN"),
        (UPC, "UPC"),
        (MANUFACTURE, "Manufacture"),
    )


class ProductDocumentTypes:
    IMAGE = "image"
    PDF = "pdf"
    QRCODE = "qrcode"

    CHOICES = (
        (IMAGE, "IMAGE"),
        (PDF, "PDF"),
        (QRCODE, "QRCODE"),
    )
