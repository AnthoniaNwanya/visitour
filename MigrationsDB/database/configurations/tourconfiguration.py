from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import ARRAY, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship


from database.base import Base


class Tour(Base):
    __tablename__ = "tours"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    agency_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("agencies.id"))
    tour_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    country: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    available_slots: Mapped[int] = mapped_column(Integer, nullable=False)
    images: Mapped[list[str]] = mapped_column(
        ARRAY(Text), nullable=False, server_default=text("'{}'::text[]")
    )
    cover_image: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str | None] = mapped_column(
        String(20), nullable=True, server_default=text("'AVAILABLE'")
    )
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, server_default=text("CURRENT_TIMESTAMP")
    )
    agency: Mapped["Agency | None"] = relationship(back_populates="tours")

    tour_bookings: Mapped[list["TourBooking"]] = relationship(
        back_populates="tour"
    )
