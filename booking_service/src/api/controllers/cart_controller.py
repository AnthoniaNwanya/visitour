from fastapi import Depends, HTTPException

from api.dependencies.authorization import get_current_traveler
from schemas.add_cart_item_request import AddCartItemRequest
from schemas.dtos.cart_response import CartResponse
from schemas.update_cart_item_request import UpdateCartItemRequest
from services.cart_service import cart_service
from services.exception.exceptions import (
    CartItemNotFoundError,
    CartItemUnavailableError,
    CartNotEditableError,
    ItemNotFoundError,
)


async def get_cart(
    traveler_id: int = Depends(get_current_traveler),
) -> CartResponse | None:
    return await cart_service.get_active_cart(traveler_id)


async def add_cart_item(
    request: AddCartItemRequest,
    traveler_id: int = Depends(get_current_traveler),
) -> CartResponse:
    try:
        return await cart_service.add_cart_item(request, traveler_id)
    except ItemNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except CartItemUnavailableError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


async def update_cart_item(
    item_id: int,
    request: UpdateCartItemRequest,
    traveler_id: int = Depends(get_current_traveler),
) -> CartResponse | None:
    try:
        return await cart_service.update_cart_item(
            item_id, traveler_id, request.quantity
        )
    except CartItemNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except CartNotEditableError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


async def delete_cart_item(
    item_id: int,
    traveler_id: int = Depends(get_current_traveler),
) -> CartResponse | None:
    try:
        return await cart_service.delete_cart_item(item_id, traveler_id)
    except CartItemNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except CartNotEditableError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
