from datetime import datetime
from pydantic import BaseModel

class AgencyLoginResponse(BaseModel):
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
    access_token: str
    token_type: str
    created_at: datetime
