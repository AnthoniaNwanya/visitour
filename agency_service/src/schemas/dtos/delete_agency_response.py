from datetime import datetime
from pydantic import BaseModel

class DeleteAgencyResponse(BaseModel):
    message: str