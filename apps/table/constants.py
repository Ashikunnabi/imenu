class TableCodeTypes:
    IAN = "ian"
    UPC = "upc"
    MANUFACTURE = "manufacture"

    CHOICES = (
        (IAN, "IAN"),
        (UPC, "UPC"),
        (MANUFACTURE, "Manufacture"),
    )


class TableDocumentTypes:
    IMAGE = "image"
    PDF = "pdf"
    QRCODE = "qrcode"

    CHOICES = (
        (IMAGE, "IMAGE"),
        (PDF, "PDF"),
        (QRCODE, "QRCODE"),
    )
