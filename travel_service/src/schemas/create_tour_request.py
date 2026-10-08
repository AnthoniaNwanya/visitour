from pydantic import BaseModel, field_validator
from datetime import date

class CreateTourRequest(BaseModel):
    title: str
    description: str
    country: list[str]
    start_date: date
    end_date: date
    price: int
    available_slots: int
    
