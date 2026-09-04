from sqlalchemy.orm import Session

from app.models import Room, Section, Subject, Timetable


def check_timetable_conflicts(
    db: Session,
    college_id: int,
    section_id: int,
    subject_id: int,
    teacher_id: int,
    room_id: int,
    day_of_week: int,
    start_time,
    end_time,
    exclude_timetable_id: int | None = None,
) -> list[str]:
    """Validate timetable conflicts before creating or updating an entry."""

    conflicts: list[str] = []

    section = db.query(Section).filter(
        Section.id == section_id,
        Section.college_id == college_id,
        Section.is_active.is_(True),
    ).first()

    subject = db.query(Subject).filter(
        Subject.id == subject_id,
        Subject.college_id == college_id,
        Subject.is_active.is_(True),
    ).first()

    room = db.query(Room).filter(
        Room.id == room_id,
        Room.college_id == college_id,
        Room.is_active.is_(True),
    ).first()

    if not section:
        conflicts.append("Section does not belong to this college or is inactive.")

    if not subject:
        conflicts.append("Subject does not belong to this college or is inactive.")

    if not room:
        conflicts.append("Room does not belong to this college or is inactive.")

    if room and section and section.capacity > room.capacity:
        conflicts.append(
            f"Room capacity ({room.capacity}) is smaller than section capacity ({section.capacity})."
        )

    if room and subject and subject.subject_type.lower() == "lab" and not room.is_lab:
        conflicts.append("Lab subject requires a laboratory room.")

    query = db.query(Timetable).filter(
        Timetable.college_id == college_id,
        Timetable.day_of_week == day_of_week,
        Timetable.is_active.is_(True),
        Timetable.start_time < end_time,
        Timetable.end_time > start_time,
    )

    if exclude_timetable_id is not None:
        query = query.filter(Timetable.id != exclude_timetable_id)

    existing_entries = query.all()

    for entry in existing_entries:
        if entry.teacher_id == teacher_id:
            conflicts.append(
                "Teacher is already assigned to another class at this time."
            )

        if entry.room_id == room_id:
            conflicts.append(
                "Room is already occupied by another class at this time."
            )

        if entry.section_id == section_id:
            conflicts.append(
                "Section already has another class at this time."
            )

    return list(dict.fromkeys(conflicts))
