from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "XXXX"
down_revision = "851da6bcf6f4"

def upgrade() -> None:
    op.alter_column(
        "outbox_events",
        "aggregate_id",
        type_=sa.Text(),
        postgresql_using="aggregate_id::text",
        existing_type=postgresql.UUID(as_uuid=True),
        nullable=False,
    )

def downgrade() -> None:
    op.alter_column(
        "outbox_events",
        "aggregate_id",
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using="aggregate_id::uuid",
        existing_type=sa.Text(),
        nullable=False,
    )
