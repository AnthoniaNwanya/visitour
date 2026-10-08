from pydantic import BaseModel, field_validator
from datetime import date
from decimal import Decimal

class CreateVisaRequest(BaseModel):
    visa_name: str
    country: str
    visa_type_id: int
    processing_time_value: int
    processing_time_unit: str
    processing_fee: Decimal

 