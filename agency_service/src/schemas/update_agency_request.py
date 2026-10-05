from pydantic import BaseModel, field_validator
from schemas.validation.validator import FieldValidator

class UpdateAgencyRequest(BaseModel):
    agency_name: str|None = None
    description: str|None = None
    first_name: str|None = None
    last_name: str|None = None
    phone_number: str|None = None
    address: str|None = None
    country: str|None = None
    city: str|None = None
    password: str|None = None
    confirm_password: str|None = None


    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):
        if value is None:
            return value

        return FieldValidator.validate_phone_number(value)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if value is None:
            return value

        return FieldValidator.validate_password(value)