from datetime import datetime

from sqlalchemy import Integer, String, Text, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Agency(Base):
    __tablename__ = "agencies"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    agency_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    first_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    address: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    status: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        server_default=text("'PENDING_VERIFICATION'")
    )

    cac_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    profilepicture: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP")
    )

    tours: Mapped[list["Tour"]] = relationship(back_populates="agency")

    visa_applications: Mapped[list["VisaApplication"]] = relationship(
        back_populates="agency"
    )

    tour_bookings: Mapped[list["TourBooking"]] = relationship(
        back_populates="agency"
    )

    visa_bookings: Mapped[list["VisaBooking"]] = relationship(
        back_populates="agency"
    )