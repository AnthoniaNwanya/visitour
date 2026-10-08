from datetime import datetime
from pydantic import BaseModel


class GetQueryResponse(BaseModel):
    id: int
    agency_id: int
    visa_name: str
    country: str
    visa_type_id: int
    processing_time_value: int
    processing_time_unit: str
    processing_fee: datetime
    status: str
    created_at: datetime
    updated_at: datetime

  
    