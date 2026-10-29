from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class UpdatePaymentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["paid", "failed", "cancelled"] | None = None
    payment_method: str | None = Field(default=None, min_length=1, max_length=50)

    @model_validator(mode="after")
    def require_update(self):
        if self.status is None and self.payment_method is None:
            raise ValueError("Provide a payment status or payment method")
        return self
