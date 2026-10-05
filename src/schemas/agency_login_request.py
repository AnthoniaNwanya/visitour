from pydantic import BaseModel

class AgencyLoginRequest(BaseModel):
    email: str
    password: str
