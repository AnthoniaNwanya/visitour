from enum import Enum


class CartStatus(str, Enum):
    ACTIVE = "active"
    PENDING_PAYMENT = "pending_payment"
    CHECKED_OUT = "checked_out"
    ABANDONED = "abandoned"
