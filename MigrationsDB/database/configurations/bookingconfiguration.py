from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint, CHAR, DateTime, ForeignKey, Integer, Numeric, String, text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="bookings_total_amount_check"),
        CheckConstraint(
            "status IN ('pending_payment', 'booked', 'cancelled')",
            name="bookings_status_check",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    traveler_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("travelers.id"), nullable=False
    )
    cart_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("carts.id", ondelete="SET NULL"), nullable=True
    )
    booking_reference: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(
        CHAR(3), nullable=False, server_default=text("'NGN'")
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'pending_payment'")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    traveler: Mapped["Traveler"] = relationship(back_populates="bookings")

    cart: Mapped["Cart | None"] = relationship(back_populates="bookings")

    tour_bookings: Mapped[list["TourBooking"]] = relationship(
        back_populates="booking",
        passive_deletes=True
    )

    visa_bookings: Mapped[list["VisaBooking"]] = relationship(
        back_populates="booking",
        passive_deletes=True
    )
