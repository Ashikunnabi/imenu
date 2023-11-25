class TableCodeTypes:
    SERIAL = "serial"
    UPC = "upc"
    MANUFACTURE = "manufacture"

    CHOICES = (
        (SERIAL, "SERIAL"),
        (UPC, "UPC"),
        (MANUFACTURE, "Manufacture"),
    )


class TableDocumentTypes:
    IMAGE = "image"
    PDF = "pdf"
    QRCODE = "qrcode"
    UNKNOWN = "unknown"

    CHOICES = (
        (IMAGE, "IMAGE"),
        (PDF, "PDF"),
        (QRCODE, "QRCODE"),
        (UNKNOWN, "UNKNOWN"),
    )
