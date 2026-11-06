from datetime import datetime
from decimal import Decimal

from sqlalchemy import ARRAY, DateTime, ForeignKey, Integer, Numeric, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class VisaApplication(Base):
    __tablename__ = "visa_applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    agency_id: Mapped[int] = mapped_column(Integer, ForeignKey("agencies.id"), nullable=False)
    visa_name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    visa_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("visa_types.id"), nullable=False
    )
    processing_time_value: Mapped[int] = mapped_column(Integer, nullable=False)
    processing_time_unit: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'DAY'")
    )
    processing_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    images: Mapped[list[str]] = mapped_column(
        ARRAY(Text), nullable=False, server_default=text("'{}'::text[]")
    )
    cover_image: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'AVAILABLE'")
    )
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, server_default=text("CURRENT_TIMESTAMP")
    )
    agency: Mapped["Agency"] = relationship(
    back_populates="visa_applications"
    )

    visa_type: Mapped["VisaType"] = relationship(
        back_populates="visa_applications"
    )

    visa_bookings: Mapped[list["VisaBooking"]] = relationship(
        back_populates="visa"
    )
