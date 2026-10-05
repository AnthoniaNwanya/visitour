from pydantic import BaseModel

class ValidateCACRequest(BaseModel):
    cac_number: str
