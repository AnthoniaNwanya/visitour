from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint, Computed, DateTime, ForeignKey, Index, Integer, Numeric,
    String, text, desc,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class VisaBooking(Base):
    __tablename__ = "visa_bookings"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="visa_bookings_quantity_check"),
        CheckConstraint("processing_fee >= 0", name="visa_bookings_processing_fee_check"),
        CheckConstraint(
            "status IN ('documents_required', 'submitted', 'in_review', 'approved', 'rejected', 'cancelled')",
            name="visa_bookings_status_check",
        ),
        Index("idx_visa_bookings_agency_created", "agency_id", desc("created_at")),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    booking_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False
    )
    visa_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("visa_applications.id"), nullable=False
    )
    agency_id: Mapped[int] = mapped_column(Integer, ForeignKey("agencies.id"), nullable=False)
    visa_name: Mapped[str] = mapped_column(String(150), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("1")
    )
    processing_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), Computed("quantity * processing_fee", persisted=True)
    )
    status: Mapped[str] = mapped_column(
        String(25), nullable=False, server_default=text("'documents_required'")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    booking: Mapped["Booking"] = relationship(back_populates="visa_bookings")

    visa: Mapped["VisaApplication"] = relationship(
        back_populates="visa_bookings"
    )

    agency: Mapped["Agency"] = relationship(back_populates="visa_bookings")
