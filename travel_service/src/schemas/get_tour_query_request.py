from pydantic import BaseModel
from datetime import date

class GetQueryRequest(BaseModel):
    id: int|None = None
    title: str|None = None
    country: str|None = None
    start_date: date|None = None
    end_date: date|None = None
    available_slots: int|None = None
    status: str|None = None
    min_price: int|None = None 
    max_price: int|None = None
    
  
