from datetime import time

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Timetable
from app.services.timetable_conflict import check_timetable_conflicts


router = APIRouter(prefix="/timetables", tags=["Timetable"])


class TimetableCreate(BaseModel):
    college_id: int = Field(gt=0)
    section_id: int = Field(gt=0)
    subject_id: int = Field(gt=0)
    teacher_id: int = Field(gt=0)
    room_id: int = Field(gt=0)
    day_of_week: int = Field(ge=1, le=7)
    start_time: time
    end_time: time
    period_number: int = Field(gt=0)
    timetable_type: str = "regular"
    notes: str | None = None


class TimetableUpdate(BaseModel):
    section_id: int = Field(gt=0)
    subject_id: int = Field(gt=0)
    teacher_id: int = Field(gt=0)
    room_id: int = Field(gt=0)
    day_of_week: int = Field(ge=1, le=7)
    start_time: time
    end_time: time
    period_number: int = Field(gt=0)
    timetable_type: str = "regular"
    notes: str | None = None


def timetable_response(timetable: Timetable) -> dict:
    return {
        "id": timetable.id,
        "college_id": timetable.college_id,
        "section_id": timetable.section_id,
        "subject_id": timetable.subject_id,
        "teacher_id": timetable.teacher_id,
        "room_id": timetable.room_id,
        "day_of_week": timetable.day_of_week,
        "start_time": timetable.start_time.isoformat(),
        "end_time": timetable.end_time.isoformat(),
        "period_number": timetable.period_number,
        "timetable_type": timetable.timetable_type,
        "notes": timetable.notes,
        "is_active": timetable.is_active,
    }


@router.get("")
def list_timetables(
    college_id: int | None = None,
    section_id: int | None = None,
    teacher_id: int | None = None,
    day_of_week: int | None = Query(default=None, ge=1, le=7),
    db: Session = Depends(get_db),
):
    query = db.query(Timetable).filter(Timetable.is_active.is_(True))

    if college_id is not None:
        query = query.filter(Timetable.college_id == college_id)
    if section_id is not None:
        query = query.filter(Timetable.section_id == section_id)
    if teacher_id is not None:
        query = query.filter(Timetable.teacher_id == teacher_id)
    if day_of_week is not None:
        query = query.filter(Timetable.day_of_week == day_of_week)

    entries = query.order_by(
        Timetable.day_of_week,
        Timetable.start_time,
        Timetable.period_number,
    ).all()

    return [timetable_response(entry) for entry in entries]


@router.get("/{timetable_id}")
def get_timetable(timetable_id: int, db: Session = Depends(get_db)):
    timetable = db.query(Timetable).filter(
        Timetable.id == timetable_id,
        Timetable.is_active.is_(True),
    ).first()

    if not timetable:
        raise HTTPException(status_code=404, detail="Timetable not found.")

    return timetable_response(timetable)


@router.post("", status_code=201)
def create_timetable(payload: TimetableCreate, db: Session = Depends(get_db)):
    if payload.start_time >= payload.end_time:
        raise HTTPException(
            status_code=400,
            detail="Start time must be earlier than end time.",
        )

    conflicts = check_timetable_conflicts(
        db=db,
        college_id=payload.college_id,
        section_id=payload.section_id,
        subject_id=payload.subject_id,
        teacher_id=payload.teacher_id,
        room_id=payload.room_id,
        day_of_week=payload.day_of_week,
        start_time=payload.start_time,
        end_time=payload.end_time,
    )

    if conflicts:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Timetable conflicts detected.",
                "conflicts": conflicts,
            },
        )

    timetable = Timetable(
        college_id=payload.college_id,
        section_id=payload.section_id,
        subject_id=payload.subject_id,
        teacher_id=payload.teacher_id,
        room_id=payload.room_id,
        day_of_week=payload.day_of_week,
        start_time=payload.start_time,
        end_time=payload.end_time,
        period_number=payload.period_number,
        timetable_type=payload.timetable_type,
        notes=payload.notes,
    )

    db.add(timetable)
    db.commit()
    db.refresh(timetable)

    return {
        "message": "Timetable created successfully.",
        "timetable": timetable_response(timetable),
    }


@router.put("/{timetable_id}")
def update_timetable(
    timetable_id: int,
    payload: TimetableUpdate,
    db: Session = Depends(get_db),
):
    timetable = db.query(Timetable).filter(
        Timetable.id == timetable_id,
        Timetable.is_active.is_(True),
    ).first()

    if not timetable:
        raise HTTPException(status_code=404, detail="Timetable not found.")

    if payload.start_time >= payload.end_time:
        raise HTTPException(
            status_code=400,
            detail="Start time must be earlier than end time.",
        )

    conflicts = check_timetable_conflicts(
        db=db,
        college_id=timetable.college_id,
        section_id=payload.section_id,
        subject_id=payload.subject_id,
        teacher_id=payload.teacher_id,
        room_id=payload.room_id,
        day_of_week=payload.day_of_week,
        start_time=payload.start_time,
        end_time=payload.end_time,
        exclude_timetable_id=timetable_id,
    )

    if conflicts:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Timetable conflicts detected.",
                "conflicts": conflicts,
            },
        )

    timetable.section_id = payload.section_id
    timetable.subject_id = payload.subject_id
    timetable.teacher_id = payload.teacher_id
    timetable.room_id = payload.room_id
    timetable.day_of_week = payload.day_of_week
    timetable.start_time = payload.start_time
    timetable.end_time = payload.end_time
    timetable.period_number = payload.period_number
    timetable.timetable_type = payload.timetable_type
    timetable.notes = payload.notes

    db.commit()
    db.refresh(timetable)

    return {
        "message": "Timetable updated successfully.",
        "timetable": timetable_response(timetable),
    }


@router.delete("/{timetable_id}")
def delete_timetable(timetable_id: int, db: Session = Depends(get_db)):
    timetable = db.query(Timetable).filter(
        Timetable.id == timetable_id,
        Timetable.is_active.is_(True),
    ).first()

    if not timetable:
        raise HTTPException(status_code=404, detail="Timetable not found.")

    timetable.is_active = False
    db.commit()

    return {
        "message": "Timetable deleted successfully.",
        "timetable_id": timetable_id,
    }
