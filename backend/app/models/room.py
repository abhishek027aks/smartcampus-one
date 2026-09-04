from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    college_id: Mapped[int] = mapped_column(
        ForeignKey("colleges.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    room_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    room_type: Mapped[str] = mapped_column(
        String(30),
        default="classroom",
        nullable=False,
    )

    capacity: Mapped[int] = mapped_column(
        Integer,
        default=60,
        nullable=False,
    )

    building: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    floor: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    is_lab: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )