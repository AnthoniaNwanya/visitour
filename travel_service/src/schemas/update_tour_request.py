from pydantic import BaseModel, field_validator
from datetime import date

class UpdateTourRequest(BaseModel):
    title: str|None = None
    description: str|None = None
    country: list[str]|None = None
    start_date: date|None = None
    end_date: date|None = None
    price: int|None = None
    available_slots: int|None = None
    status: str|None = None
    
