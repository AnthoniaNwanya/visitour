from datetime import datetime

from pydantic import BaseModel


class VisaTypeResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime