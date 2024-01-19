class OrderStatus:
    CREATED = "created"
    PAYMENT_PENDING = "payment_pending"
    NEW = "new"
    PROCESSING = "processing"
    PROCESSED = "processed"
    ERROR = "error"
    DELIVERED = "delivered"
    CANCELED = "canceled"
    REFUNDED = "refunded"

    CHOICES = (
        (CREATED, "Created"),
        (PAYMENT_PENDING, "Payment pending"),
        (NEW, "New"),
        (PROCESSING, "Processing"),
        (PROCESSED, "Processed"),
        (ERROR, "Error"),
        (DELIVERED, "Delivered"),
        (CANCELED, "Canceled"),
        (REFUNDED, "Refunded"),
    )


class OrderLineStatus:
    CREATED = "created"
    PAYMENT_PENDING = "payment_pending"
    NEW = "new"
    PROCESSING = "processing"
    PROCESSED = "processed"
    ERROR = "error"
    DELIVERED = "delivered"
    CANCELED = "canceled"
    REFUNDED = "refunded"

    CHOICES = (
        (CREATED, "Created"),
        (PAYMENT_PENDING, "Payment pending"),
        (NEW, "New"),
        (PROCESSING, "Processing"),
        (PROCESSED, "Processed"),
        (ERROR, "Error"),
        (DELIVERED, "Delivered"),
        (CANCELED, "Canceled"),
        (REFUNDED, "Refunded"),
    )
