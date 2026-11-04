from pydantic import BaseModel, Field, model_validator
from datetime import date
from decimal import Decimal

class CreateVisaRequest(BaseModel):
    visa_name: str
    country: str
    visa_type_id: int
    processing_time_value: int
    processing_time_unit: str
    processing_fee: Decimal
    images: list[str] = Field(default_factory=list)
    cover_image: str | None = None

    @model_validator(mode="after")
    def validate_cover_image(self):
        if self.images and not self.cover_image:
            raise ValueError("cover_image is required when images are provided")
        if self.cover_image and self.cover_image not in self.images:
            raise ValueError("cover_image must be one of images")
        return self

 