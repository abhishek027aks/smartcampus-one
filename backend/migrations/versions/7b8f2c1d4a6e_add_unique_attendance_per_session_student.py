"""add unique attendance per session and student

Revision ID: 7b8f2c1d4a6e
Revises: 139ac5cfac2d
"""

from typing import Sequence, Union

from alembic import op


revision: str = "7b8f2c1d4a6e"
down_revision: Union[str, Sequence[str], None] = "139ac5cfac2d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_attendance_records_session_student",
        "attendance_records",
        ["session_id", "student_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_attendance_records_session_student",
        "attendance_records",
        type_="unique",
    )
