from enum import Enum


class ProcessingTimeUnit(str, Enum):
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"