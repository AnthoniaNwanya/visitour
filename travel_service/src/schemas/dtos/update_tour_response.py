from datetime import datetime
from pydantic import BaseModel

class UpdateTourResponse(BaseModel):
    id: int
    agency_id: int
    tour_name: str
    description: str
    country: list[str]
    start_date: datetime
    end_date: datetime
    price: int
    available_slots: int
    images: list[str]
    cover_image: str | None = None
    status: str
    updated_at: datetime
