"""add device session id to attendance records

Revision ID: 8c9d3e2f5a71
Revises: 7b8f2c1d4a6e
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8c9d3e2f5a71"
down_revision: Union[str, Sequence[str], None] = "7b8f2c1d4a6e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "attendance_records",
        sa.Column("device_session_id", sa.String(length=128), nullable=True),
    )
    op.create_index(
        "ix_attendance_records_device_session_id",
        "attendance_records",
        ["device_session_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_attendance_records_device_session_id",
        table_name="attendance_records",
    )
    op.drop_column(
        "attendance_records",
        "device_session_id",
    )
