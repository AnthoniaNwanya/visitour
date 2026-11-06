from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint, DateTime, ForeignKey, Index, Integer, Numeric, String, text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Cart(Base):
    __tablename__ = "carts"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'pending_payment', 'checked_out', 'abandoned')",
            name="ck_carts_status",
        ),
        CheckConstraint(
            "total_order_summary >= 0", name="carts_total_order_summary_check"
        ),
        Index(
            "uq_traveler_active_cart",
            "traveler_id",
            unique=True,
            postgresql_where=text("status = 'active'"),
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    traveler_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("travelers.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'active'")
    )
    total_order_summary: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, server_default=text("0")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    traveler: Mapped["Traveler"] = relationship(back_populates="carts")

    cart_items: Mapped[list["CartItem"]] = relationship(
        back_populates="cart",
        passive_deletes=True
    )

    bookings: Mapped[list["Booking"]] = relationship(back_populates="cart")

    payments: Mapped[list["Payment"]] = relationship(back_populates="cart")
