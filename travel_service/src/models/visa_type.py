from datetime import datetime
from models.enums.visa_status import VisaStatus
from models.enums.processing_time_unit import ProcessingTimeUnit


class VisaApplication:
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        created_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

