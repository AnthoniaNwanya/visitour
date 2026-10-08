from pydantic import BaseModel
from datetime import date

class VisaQueryRequest(BaseModel):
    id: int | None = None
    visa_name: str | None = None
    country: str | None = None
    visa_type_id: int | None = None
