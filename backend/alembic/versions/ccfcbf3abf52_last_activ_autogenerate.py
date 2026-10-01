"""last activ - autogenerate

Revision ID: ccfcbf3abf52
Revises: 90c18a706bb9
Create Date: 2026-09-30 12:22:04.742190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccfcbf3abf52'
down_revision: Union[str, Sequence[str], None] = '90c18a706bb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [c["name"] for c in inspector.get_columns("task_board")]
    if "last_activity_at" not in columns:
        op.add_column(
            "task_board",
            sa.Column("last_activity_at", sa.DateTime(timezone=True), nullable=True),
        )


def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [c["name"] for c in inspector.get_columns("task_board")]
    if "last_activity_at" in columns:
        op.drop_column("task_board", "last_activity_at")