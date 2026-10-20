
from pydantic import BaseModel, field_validator
from schemas.validation.validator import FieldValidator


class TravelerLoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        return FieldValidator.validate_email(str(value))

    @field_validator("password", mode="before")
    @classmethod
    def validate_password_not_empty(cls, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Password cannot be empty")

        return value