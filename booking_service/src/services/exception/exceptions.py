class ValueRequiredError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class BookingAlreadyExistsError(Exception):
    pass


class BookingNotFoundError(Exception):
    pass


class ItemNotFoundError(Exception):
    pass


class BookingNotEditableError(Exception):
    pass


class CartItemNotFoundError(Exception):
    pass


class CartNotFoundError(Exception):
    pass


class CartNotEditableError(Exception):
    pass


class CartItemUnavailableError(Exception):
    pass


class CartPriceChangedError(Exception):
    pass


class PaymentNotFoundError(Exception):
    pass


class PaymentNotEditableError(Exception):
    pass
