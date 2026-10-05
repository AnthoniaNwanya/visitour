from enum import Enum


class AgencyStatus(str, Enum):
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"
    DELETED = 'DELETED'
    INACTIVE = 'INACTIVE'