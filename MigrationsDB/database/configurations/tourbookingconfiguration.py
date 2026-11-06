from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint, Computed, DateTime, ForeignKey, Integer, Index, Numeric,
    String, text, desc,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class TourBooking(Base):
    __tablename__ = "tour_bookings"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="tour_bookings_quantity_check"),
        CheckConstraint("unit_price >= 0", name="tour_bookings_unit_price_check"),
        CheckConstraint(
            "status IN ('pending_confirmation', 'confirmed', 'in_progress', 'completed', 'cancelled')",
            name="tour_bookings_status_check",
        ),
        Index("idx_tour_bookings_agency_created", "agency_id", desc("created_at")),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    booking_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False
    )
    tour_id: Mapped[int] = mapped_column(Integer, ForeignKey("tours.id"), nullable=False)
    agency_id: Mapped[int] = mapped_column(Integer, ForeignKey("agencies.id"), nullable=False)
    tour_name: Mapped[str] = mapped_column(String(150), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("1"))
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), Computed("quantity * unit_price", persisted=True)
    )
    status: Mapped[str] = mapped_column(
        String(25), nullable=False, server_default=text("'pending_confirmation'")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    booking: Mapped["Booking"] = relationship(back_populates="tour_bookings")

    tour: Mapped["Tour"] = relationship(back_populates="tour_bookings")

    agency: Mapped["Agency"] = relationship(back_populates="tour_bookings")
