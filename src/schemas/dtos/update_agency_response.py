from datetime import datetime
from pydantic import BaseModel

class UpdateAgencyResponse(BaseModel):
    id: int
    agency_name: str
    description: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    address: str
    country: str
    city: str
    cac_number: str
    status: str
    updated_at: datetime
    