from schemas.add_cart_item_request import AddCartItemRequest
from schemas.dtos.cart_response import CartResponse
from repository.cart_repository import CartRepository


class CartService:
    def __init__(self):
        self.repository = CartRepository()

    async def get_active_cart(self, traveler_id: int) -> CartResponse | None:
        cart = await self.repository.get_active_cart(traveler_id)
        if cart is None:
            return None
        return CartResponse.model_validate(cart)

    async def add_cart_item(
        self, payload: AddCartItemRequest, traveler_id: int
    ) -> CartResponse:
        cart = await self.repository.add_item(payload, traveler_id)
        return CartResponse.model_validate(cart)

    async def update_cart_item(
        self, item_id: int, traveler_id: int, quantity: int
    ) -> CartResponse | None:
        cart = await self.repository.update_item(item_id, traveler_id, quantity)
        if cart is None:
            return None
        return CartResponse.model_validate(cart)

    async def delete_cart_item(
        self, item_id: int, traveler_id: int
    ) -> CartResponse | None:
        cart = await self.repository.delete_item(item_id, traveler_id)
        if cart is None:
            return None
        return CartResponse.model_validate(cart)


cart_service = CartService()
