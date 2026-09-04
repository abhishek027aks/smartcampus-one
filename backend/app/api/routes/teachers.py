from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.routes.auth import get_current_user, require_roles
from app.core.database import get_db
from app.models import Section, Subject, Teacher, TeacherSubject

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.get("/me")
def get_my_teacher(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("teacher")),
):
    teacher = (
        db.query(Teacher)
        .filter(
            Teacher.user_id == current_user.id,
            Teacher.college_id == current_user.college_id,
            Teacher.is_active.is_(True),
        )
        .first()
    )

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found.")

    return {
        "id": teacher.id,
        "user_id": teacher.user_id,
        "college_id": teacher.college_id,
        "department_id": teacher.department_id,
        "employee_id": teacher.employee_id,
        "designation": teacher.designation,
        "joining_date": teacher.joining_date,
        "is_active": teacher.is_active,
    }


@router.get("/me/subjects")
def get_my_subjects(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("teacher")),
):
    teacher = (
        db.query(Teacher)
        .filter(
            Teacher.user_id == current_user.id,
            Teacher.college_id == current_user.college_id,
            Teacher.is_active.is_(True),
        )
        .first()
    )

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found.")

    rows = (
        db.query(Subject)
        .join(TeacherSubject, TeacherSubject.subject_id == Subject.id)
        .filter(
            TeacherSubject.teacher_id == teacher.id,
            Subject.college_id == current_user.college_id,
            Subject.is_active.is_(True),
        )
        .order_by(Subject.semester, Subject.code)
        .all()
    )

    return [
        {
            "id": subject.id,
            "code": subject.code,
            "name": subject.name,
            "semester": subject.semester,
            "credits": subject.credits,
            "subject_type": subject.subject_type,
        }
        for subject in rows
    ]


@router.get("/me/sections")
def get_my_sections(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("teacher")),
):
    teacher = (
        db.query(Teacher)
        .filter(
            Teacher.user_id == current_user.id,
            Teacher.college_id == current_user.college_id,
            Teacher.is_active.is_(True),
        )
        .first()
    )

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found.")

    sections = (
        db.query(Section)
        .filter(
            Section.college_id == current_user.college_id,
            Section.is_active.is_(True),
        )
        .order_by(Section.semester, Section.name)
        .all()
    )

    return [
        {
            "id": section.id,
            "course_id": section.course_id,
            "name": section.name,
            "semester": section.semester,
            "academic_year": section.academic_year,
            "capacity": section.capacity,
        }
        for section in sections
    ]
