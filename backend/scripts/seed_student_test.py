import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models import User, Student


db = SessionLocal()

try:
    user = db.query(User).filter(
        User.email == "student.test@smartcampus.local"
    ).first()

    if not user:
        user = User(
            college_id=1,
            full_name="Test Student",
            email="student.test@smartcampus.local",
            password_hash=hash_password("Student@123"),
            role="student",
            is_active=True,
        )
        db.add(user)
        db.flush()
    else:
        user.password_hash = hash_password("Student@123")
        user.role = "student"
        user.college_id = 1
        user.is_active = True

    student = db.query(Student).filter(
        Student.user_id == user.id
    ).first()

    if not student:
        student = Student(
            user_id=user.id,
            college_id=1,
            course_id=1,
            section_id=1,
            enrollment_number="TEST-S001",
            admission_year=2026,
            current_semester=1,
            is_active=True,
        )
        db.add(student)

    db.commit()
    db.refresh(user)
    db.refresh(student)

    print("STUDENT SEED: OK")
    print("user_id:", user.id)
    print("student_id:", student.id)
    print("email:", user.email)
    print("role:", user.role)
    print("section_id:", student.section_id)
    print("enrollment:", student.enrollment_number)

finally:
    db.close()
