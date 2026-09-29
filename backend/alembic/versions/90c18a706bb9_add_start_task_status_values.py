"""add start task status values

Revision ID: 90c18a706bb9
Revises: 00e9e6ee9e59
Create Date: 2026-09-29 11:15:27.129370

"""
from typing import Sequence, Union
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90c18a706bb9'
down_revision: Union[str, Sequence[str], None] = '00e9e6ee9e59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Определяем таблицу для bulk_insert (только нужные колонки)
task_status_table = sa.table(
    "task_status",
    sa.column("name", sa.String),
    sa.column("description", sa.String),
    sa.column("is_default", sa.Boolean),
    sa.column("is_final", sa.Boolean),
    sa.column("is_active", sa.Boolean),
    sa.column("create_at", sa.DateTime(timezone=True)),
)


def upgrade() -> None:
    """Upgrade schema."""
    now = datetime.now(timezone.utc)
    
    op.bulk_insert(
        task_status_table,
        [
            {
                "name": "todo",
                "description": "Задача в очереди, ещё не начата",
                "is_default": True,
                "is_final": False,
                "is_active": True,
                "create_at": now,
            },
            {
                "name": "in_progress",
                "description": "Задача в работе",
                "is_default": False,
                "is_final": False,
                "is_active": True,
                "create_at": now,
            },
            {
                "name": "testing",
                "description": "Задача на тестировании",
                "is_default": False,
                "is_final": False,
                "is_active": True,
                "create_at": now,
            },
            {
                "name": "done",
                "description": "Задача успешно завершена",
                "is_default": False,
                "is_final": True,
                "is_active": True,
                "create_at": now,
            },
            {
                "name": "cancelled",
                "description": "Задача отменена",
                "is_default": False,
                "is_final": True,
                "is_active": True,
                "create_at": now,
            },
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            "DELETE FROM task_status WHERE name IN "
            "('todo', 'in_progress', 'testing', 'done', 'cancelled')"
        )
    )