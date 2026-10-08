from datetime import datetime
from pydantic import BaseModel


class GetQueryResponse(BaseModel):
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
    created_at: datetime
    updated_at: datetime

  
    