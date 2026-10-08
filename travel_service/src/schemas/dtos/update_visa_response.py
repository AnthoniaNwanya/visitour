from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal

class UpdateVisaResponse(BaseModel):
    id: int
    agency_id: int
    visa_name: str
    country: str
    visa_type_id: int
    processing_time_value: int
    processing_time_unit: str
    processing_fee: Decimal
    status: str
    updated_at: datetime

  
    