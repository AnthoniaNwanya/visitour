from datetime import datetime
from decimal import Decimal
from models.enums.visa_status import VisaStatus
from models.enums.processing_time_unit import ProcessingTimeUnit


class VisaApplication:
    def __init__(
        self,
        id: int,
        agency_id: int,
        visa_name: str,
        country: str,
        visa_type_id: int,
        processing_time_value: int,
        processing_time_unit: ProcessingTimeUnit,
        processing_fee: Decimal,
        status: VisaStatus,
        created_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.agency_id = agency_id
        self.visa_name = visa_name
        self.country = country
        self.visa_type_id = visa_type_id
        self.processing_time_value = processing_time_value
        self.processing_time_unit = processing_time_unit
        self.processing_fee = processing_fee
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

