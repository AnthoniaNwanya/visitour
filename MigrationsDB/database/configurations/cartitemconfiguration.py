from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint, Computed, DateTime, ForeignKey, Integer, Numeric,
    String, UniqueConstraint, text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class CartItem(Base):
    __tablename__ = "cart_items"
    __table_args__ = (
        CheckConstraint("booking_type IN ('tour', 'visa')", name="cart_items_booking_type_check"),
        CheckConstraint("quantity > 0", name="cart_items_quantity_check"),
        CheckConstraint("unit_price >= 0", name="cart_items_unit_price_check"),
        UniqueConstraint("cart_id", "booking_type", "item_id", name="uq_cart_item"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cart_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False
    )
    booking_type: Mapped[str] = mapped_column(String(10), nullable=False)
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    item_name: Mapped[str] = mapped_column(String(150), nullable=False)
    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("1")
    )
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), Computed("quantity * unit_price", persisted=True)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    cart: Mapped["Cart"] = relationship(back_populates="cart_items")
