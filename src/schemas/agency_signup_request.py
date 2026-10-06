from pydantic import BaseModel, field_validator
from schemas.validation.validator import FieldValidator

class AgencySignupRequest(BaseModel):
    agency_name: str
    description: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    address: str
    country: str
    city: str
    cac_number: str | None = None
    password: str
    confirm_password: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        return FieldValidator.validate_email(value)

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, value):
        return FieldValidator.validate_phone_number(value)

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        return FieldValidator.validate_password(value)