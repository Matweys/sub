# products/models.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, DateTime, Enum, CheckConstraint, text
from datetime import datetime
import enum

from database.db import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    owner: Mapped[str] = mapped_column(String(100), nullable=False)


class EventType(enum.Enum):
    online = "online"
    offline = "offline"
    hybrid = "hybrid"


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    event_type: Mapped[EventType] = mapped_column(
        Enum(EventType, name="event_type_enum"),
        nullable=False,
        server_default=text("'online'")
    )

    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    capacity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint("capacity >= 1", name="capacity_big_one"),
        CheckConstraint("price >= 0", name="price_bit_zero"),
        CheckConstraint("start_at >= now()", name="start_at_now"),
        CheckConstraint("end_at > start_at", name="end_at_start_at"),
    )
