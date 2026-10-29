from fastapi import Depends, HTTPException, Response, status

from api.dependencies.authorization import get_current_traveler
from schemas.create_payment_request import CreatePaymentRequest
from schemas.dtos.payment_response import PaymentResponse
from schemas.update_payment_request import UpdatePaymentRequest
from services.exception.exceptions import (
    CartItemUnavailableError,
    CartNotEditableError,
    CartNotFoundError,
    CartPriceChangedError,
    ItemNotFoundError,
    PaymentNotEditableError,
    PaymentNotFoundError,
)
from services.payment_service import payment_service


async def create_payment(
    request: CreatePaymentRequest,
    traveler_id: int = Depends(get_current_traveler),
) -> PaymentResponse:
    try:
        return await payment_service.create_payment(
            request.cart_id, traveler_id, request.payment_method
        )
    except CartNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ItemNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (
        CartNotEditableError,
        CartPriceChangedError,
        CartItemUnavailableError,
    ) as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


async def get_payments(
    traveler_id: int = Depends(get_current_traveler),
) -> list[PaymentResponse]:
    return await payment_service.get_payments(traveler_id)


async def get_payment(
    payment_id: int,
    traveler_id: int = Depends(get_current_traveler),
) -> PaymentResponse:
    try:
        return await payment_service.get_payment(payment_id, traveler_id)
    except PaymentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


async def update_payment(
    payment_id: int,
    request: UpdatePaymentRequest,
    traveler_id: int = Depends(get_current_traveler),
) -> PaymentResponse:
    try:
        return await payment_service.update_payment(
            payment_id,
            traveler_id,
            request.status,
            request.payment_method,
        )
    except PaymentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (
        CartNotEditableError,
        CartPriceChangedError,
        CartItemUnavailableError,
        PaymentNotEditableError,
    ) as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ItemNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


async def delete_payment(
    payment_id: int,
    traveler_id: int = Depends(get_current_traveler),
) -> Response:
    try:
        await payment_service.delete_payment(payment_id, traveler_id)
    except PaymentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PaymentNotEditableError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
