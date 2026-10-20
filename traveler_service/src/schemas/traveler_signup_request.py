from datetime import date

from pydantic import BaseModel, field_validator, model_validator
from schemas.validation.validator import FieldValidator


class TravelerSignupRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str
    confirm_password: str
    date_of_birth: date
    address: str
    city: str
    country: str
    nationality: str

    @field_validator(
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "password",
        "confirm_password",
        "nationality",
        mode="before",
    )
    @classmethod
    def check_empty_fields(cls, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("This field cannot be empty")

        return value.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        return FieldValidator.validate_email(value)

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):
        return FieldValidator.validate_phone_number(value)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        return FieldValidator.validate_password(value)

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Password and Confirm Password do not match")

        return self