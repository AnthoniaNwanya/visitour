from pydantic import BaseModel
from datetime import date

class GetQueryRequest(BaseModel):
    id: int|None = None
    agency_name: str|None = None
    email: str|None = None
    country: str|None = None
    city: str|None = None
    status: str|None = None
    cac_number: str|None = None
    start_date: date|None = None
    end_date: date|None = None
    
  