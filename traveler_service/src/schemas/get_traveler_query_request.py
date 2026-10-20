from pydantic import BaseModel
from datetime import date

class GetTravelerQueryRequest(BaseModel):
    id: int|None = None
    first_name: str|None = None
    last_name: str|None = None
    email: str|None = None
    city: str|None = None
    country: str|None = None
    nationality: str|None = None
    status: str|None = None

    
  
