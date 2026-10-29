from pydantic import BaseModel, ConfigDict, Field


class CreatePaymentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cart_id: int = Field(gt=0)
    payment_method: str = Field(default="manual", min_length=1, max_length=50)
