"""add attendance sessions and records

Revision ID: 139ac5cfac2d
Revises: e6a5a4ff7064
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "139ac5cfac2d"
down_revision: Union[str, Sequence[str], None] = "e6a5a4ff7064"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "attendance_sessions",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("college_id", sa.Integer(), nullable=False),
        sa.Column("section_id", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("teacher_id", sa.Integer(), nullable=False),
        sa.Column("session_code", sa.String(length=20), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("closed_at", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["college_id"], ["colleges.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["section_id"], ["sections.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["subject_id"], ["subjects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["teacher_id"], ["teachers.id"], ondelete="CASCADE"),
    )

    op.create_index(
        "ix_attendance_sessions_id",
        "attendance_sessions",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_attendance_sessions_college_id",
        "attendance_sessions",
        ["college_id"],
        unique=False,
    )
    op.create_index(
        "ix_attendance_sessions_section_id",
        "attendance_sessions",
        ["section_id"],
        unique=False,
    )
    op.create_index(
        "ix_attendance_sessions_subject_id",
        "attendance_sessions",
        ["subject_id"],
        unique=False,
    )
    op.create_index(
        "ix_attendance_sessions_teacher_id",
        "attendance_sessions",
        ["teacher_id"],
        unique=False,
    )
    op.create_index(
        "ix_attendance_sessions_session_code",
        "attendance_sessions",
        ["session_code"],
        unique=False,
    )
    op.create_index(
        "ix_attendance_sessions_is_active",
        "attendance_sessions",
        ["is_active"],
        unique=False,
    )

    op.create_table(
        "attendance_records",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("college_id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("marked_at", sa.DateTime(), nullable=False),
        sa.Column("live_photo_path", sa.String(length=500), nullable=True),
        sa.Column("location_latitude", sa.String(length=30), nullable=True),
        sa.Column("location_longitude", sa.String(length=30), nullable=True),
        sa.Column("verification_method", sa.String(length=30), nullable=False),
        sa.Column("notes", sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(["college_id"], ["colleges.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["attendance_sessions.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["students.id"],
            ondelete="CASCADE",
        ),
    )

    op.create_index(
        "ix_attendance_records_id",
        "attendance_records",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_attendance_records_college_id",
        "attendance_records",
        ["college_id"],
        unique=False,
    )
    op.create_index(
        "ix_attendance_records_session_id",
        "attendance_records",
        ["session_id"],
        unique=False,
    )
    op.create_index(
        "ix_attendance_records_student_id",
        "attendance_records",
        ["student_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_attendance_records_student_id",
        table_name="attendance_records",
    )
    op.drop_index(
        "ix_attendance_records_session_id",
        table_name="attendance_records",
    )
    op.drop_index(
        "ix_attendance_records_college_id",
        table_name="attendance_records",
    )
    op.drop_index(
        "ix_attendance_records_id",
        table_name="attendance_records",
    )
    op.drop_table("attendance_records")

    op.drop_index(
        "ix_attendance_sessions_is_active",
        table_name="attendance_sessions",
    )
    op.drop_index(
        "ix_attendance_sessions_session_code",
        table_name="attendance_sessions",
    )
    op.drop_index(
        "ix_attendance_sessions_teacher_id",
        table_name="attendance_sessions",
    )
    op.drop_index(
        "ix_attendance_sessions_subject_id",
        table_name="attendance_sessions",
    )
    op.drop_index(
        "ix_attendance_sessions_section_id",
        table_name="attendance_sessions",
    )
    op.drop_index(
        "ix_attendance_sessions_college_id",
        table_name="attendance_sessions",
    )
    op.drop_index(
        "ix_attendance_sessions_id",
        table_name="attendance_sessions",
    )
    op.drop_table("attendance_sessions")
