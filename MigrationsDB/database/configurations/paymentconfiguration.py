from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint, DateTime, ForeignKey, Index, Integer, Numeric, String, text, desc
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        CheckConstraint("amount >= 0", name="payments_amount_check"),
        CheckConstraint(
            "status IN ('pending', 'paid', 'failed', 'cancelled')",
            name="payments_status_check",
        ),
        Index(
            "uq_pending_payment_cart",
            "cart_id",
            unique=True,
            postgresql_where=text("cart_id IS NOT NULL AND status = 'pending'"),
        ),
        Index("idx_payments_cart_created", "cart_id",  desc("created_at")),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cart_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("carts.id", ondelete="SET NULL"), nullable=True
    )
    payment_reference: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(
        String(3), nullable=False, server_default=text("'NGN'")
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'pending'")
    )
    payment_method: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default=text("'manual'")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    cart: Mapped["Cart | None"] = relationship(back_populates="payments")
