from datetime import datetime, date
from pydantic import BaseModel

class TravelerLoginResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str 
    date_of_birth: date 
    address: str
    city: str
    country: str
    nationality: str
    status: str
    access_token: str
    token_type: str
    created_at: datetime
