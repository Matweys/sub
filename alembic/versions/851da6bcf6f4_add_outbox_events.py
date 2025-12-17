"""add outbox events

Revision ID: 851da6bcf6f4
Revises: d3833865d8bd
Create Date: 2025-12-17 20:45:31.696785
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "851da6bcf6f4"
down_revision: Union[str, Sequence[str], None] = "d3833865d8bd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "outbox_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),

        sa.Column("topic", sa.String(length=255), nullable=False),
        sa.Column("key", sa.String(length=255), nullable=True),

        sa.Column("event_type", sa.String(length=255), nullable=False),
        sa.Column("aggregate_type", sa.String(length=255), nullable=False),
        sa.Column("aggregate_id", postgresql.UUID(as_uuid=True), nullable=False),

        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),

        sa.Column("status", sa.String(length=32), nullable=False, server_default=sa.text("'pending'")),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default=sa.text("0")),

        sa.Column("available_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("locked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("locked_by", sa.String(length=255), nullable=True),

        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),

        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_index(
        "ix_outbox_events_status_available_at",
        "outbox_events",
        ["status", "available_at"],
    )
    op.create_index(
        "ix_outbox_events_locked_at",
        "outbox_events",
        ["locked_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_outbox_events_locked_at", table_name="outbox_events")
    op.drop_index("ix_outbox_events_status_available_at", table_name="outbox_events")
    op.drop_table("outbox_events")
