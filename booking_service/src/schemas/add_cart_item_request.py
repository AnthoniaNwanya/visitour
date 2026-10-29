from pydantic import BaseModel, ConfigDict, Field

from models.enums.booking_type import BookingType


class AddCartItemRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    booking_type: BookingType
    item_id: int = Field(gt=0)
    quantity: int = Field(default=1, gt=0)
