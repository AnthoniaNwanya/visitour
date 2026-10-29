from repository.payment_repository import PaymentRepository
from schemas.dtos.payment_response import PaymentResponse
from services.exception.exceptions import PaymentNotFoundError


class PaymentService:
    def __init__(self):
        self.repository = PaymentRepository()

    async def create_payment(
        self, cart_id: int, traveler_id: int, payment_method: str
    ) -> PaymentResponse:
        payment = await self.repository.create(
            cart_id, traveler_id, payment_method
        )
        return PaymentResponse.model_validate(dict(payment))

    async def get_payments(self, traveler_id: int) -> list[PaymentResponse]:
        payments = await self.repository.get_all(traveler_id)
        return [PaymentResponse.model_validate(dict(p)) for p in payments]

    async def get_payment(
        self, payment_id: int, traveler_id: int
    ) -> PaymentResponse:
        payment = await self.repository.get_by_id(payment_id, traveler_id)
        if payment is None:
            raise PaymentNotFoundError("Payment not found")
        return PaymentResponse.model_validate(dict(payment))

    async def update_payment(
        self,
        payment_id: int,
        traveler_id: int,
        status: str | None,
        payment_method: str | None,
    ) -> PaymentResponse:
        payment = await self.repository.update(
            payment_id, traveler_id, status, payment_method
        )
        return PaymentResponse.model_validate(dict(payment))

    async def delete_payment(self, payment_id: int, traveler_id: int) -> None:
        await self.repository.delete(payment_id, traveler_id)


payment_service = PaymentService()
