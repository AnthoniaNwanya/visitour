from datetime import datetime, date
from pydantic import BaseModel

class UpdateTravelerResponse(BaseModel):
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
    updated_at: datetime
    