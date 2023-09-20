class TableCodeTypes:
    SERIAL = "serial"
    UPC = "upc"
    MANUFACTURE = "manufacture"
    SERIAL = "serial"

    CHOICES = (
        (SERIAL, "SERIAL"),
        (UPC, "UPC"),
        (MANUFACTURE, "Manufacture"),
        (SERIAL, "SERIAL"),
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
