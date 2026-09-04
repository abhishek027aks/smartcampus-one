from datetime import datetime, time

from sqlalchemy import DateTime, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Timetable(Base):
    __tablename__ = "timetables"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    college_id: Mapped[int] = mapped_column(
        ForeignKey("colleges.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    section_id: Mapped[int] = mapped_column(
        ForeignKey("sections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    day_of_week: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    start_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    end_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    period_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    timetable_type: Mapped[str] = mapped_column(
        String(20),
        default="regular",
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
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