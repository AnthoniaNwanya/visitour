from datetime import datetime
from models.enums.agency_status import AgencyStatus

class Agency:
    def __init__(
        self,
        id: int,
        agency_name: str,
        description: str,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        address: str,
        city: str,
        country: str,
        status: AgencyStatus,
        cac_number: str,
        password_hash: str,
        created_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.agency_name = agency_name
        self.description = description
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.city = city
        self.country = country
        self.status = status
        self.cac_number = cac_number
        self.password_hash = password_hash
        self.created_at = created_at
        self.updated_at = updated_at

