from app.core.database import SessionLocal
from app.models import College, Department, Course, Section, User, Teacher, Subject, Room


db = SessionLocal()

try:
    college = db.query(College).filter(College.college_code == "TEST-SC1").first()
    if not college:
        college = College(college_code="TEST-SC1", name="SmartCampus Test College")
        db.add(college)
        db.flush()

    department = db.query(Department).filter(Department.college_id == college.id).first()
    if not department:
        department = Department(college_id=college.id, name="Computer Science", code="CSE")
        db.add(department)
        db.flush()

    course = db.query(Course).filter(Course.college_id == college.id).first()
    if not course:
        course = Course(college_id=college.id, department_id=department.id, name="BCA", code="BCA", duration_years=3)
        db.add(course)
        db.flush()

    section = db.query(Section).filter(Section.college_id == college.id).first()
    if not section:
        section = Section(college_id=college.id, course_id=course.id, name="A", semester=1, academic_year="2026-27", capacity=60)
        db.add(section)
        db.flush()

    teacher_user = db.query(User).filter(User.email == "teacher.test@smartcampus.local").first()
    if not teacher_user:
        teacher_user = User(college_id=college.id, full_name="Test Teacher", email="teacher.test@smartcampus.local", password_hash="TEST_ONLY", role="teacher")
        db.add(teacher_user)
        db.flush()

    teacher = db.query(Teacher).filter(Teacher.user_id == teacher_user.id).first()
    if not teacher:
        teacher = Teacher(college_id=college.id, user_id=teacher_user.id, department_id=department.id, employee_id="TEST-T001", designation="Assistant Professor")
        db.add(teacher)
        db.flush()

    subject = db.query(Subject).filter(Subject.college_id == college.id).first()
    if not subject:
        subject = Subject(college_id=college.id, department_id=department.id, course_id=course.id, code="BCA101", name="Programming Fundamentals", semester=1, credits=4, subject_type="theory")
        db.add(subject)
        db.flush()

    room = db.query(Room).filter(Room.college_id == college.id).first()
    if not room:
        room = Room(college_id=college.id, room_number="TEST-101", name="Test Classroom", room_type="classroom", capacity=60, building="Main Block", floor=1, is_lab=False)
        db.add(room)
        db.flush()

    db.commit()

    print("TEST DATA CREATED")
    print(f"college_id={college.id}")
    print(f"section_id={section.id}")
    print(f"subject_id={subject.id}")
    print(f"teacher_id={teacher.id}")
    print(f"room_id={room.id}")

finally:
    db.close()
