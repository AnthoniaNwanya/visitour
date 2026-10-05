import re


class FieldValidator:

    @staticmethod
    def validate_email(email: str) -> str:
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.match(pattern, email):
            raise ValueError("Invalid email address")

        return email

    @staticmethod
    def validate_password(password: str) -> str:
        if len(password) < 8:
            raise ValueError(
                "Password must be at least 8 characters long"
            )

        if not re.search(r"[A-Z]", password):
            raise ValueError(
                "Password must contain at least one uppercase letter"
            )

        if not re.search(r"[a-z]", password):
            raise ValueError(
                "Password must contain at least one lowercase letter"
            )

        if not re.search(r"\d", password):
            raise ValueError(
                "Password must contain at least one number"
            )

        return password

    @staticmethod
    def validate_phone_number(phone_number: str) -> str:
        pattern = r"^\+?[0-9]{10,15}$"

        if not re.match(pattern, phone_number):
            raise ValueError("Invalid phone number")

        return phone_number