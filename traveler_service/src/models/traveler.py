from datetime import datetime, date
from models.enums.traveler_status import TravelerStatus

class Traveler:
    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        password_hash: str,
        date_of_birth: date,
        address: str,
        city: str,
        country: str,
        nationality: str,
        status: TravelerStatus,
        created_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.password_hash = password_hash
        self.date_of_birth = date_of_birth
        self.address = address
        self.city = city
        self.country = country
        self.nationality = nationality
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

