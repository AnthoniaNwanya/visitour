from datetime import datetime
from pydantic import BaseModel

class UpdateTourResponse(BaseModel):
    id: int
    agency_id: int
    title: str
    description: str
    country: list[str]
    start_date: datetime
    end_date: datetime
    price: int
    available_slots: int
    status: str
    updated_at: datetime
