from datetime import datetime
from pydantic import BaseModel

class AgencySignupResponse(BaseModel):
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
    created_at: datetime
