"""recommendation text to jsonb

Revision ID: c3f1a2b4d8e0
Revises: 41aeed6c5b1b
Create Date: 2026-08-11 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c3f1a2b4d8e0"
down_revision: Union[str, Sequence[str], None] = "41aeed6c5b1b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cast recommendation to JSONB, wrapping plain text with to_jsonb()."""
    op.execute(
        """
        ALTER TABLE disease_detections
        ALTER COLUMN recommendation
        TYPE jsonb
        USING to_jsonb(recommendation)
        """
    )


def downgrade() -> None:
    """Revert JSONB back to TEXT."""
    op.execute(
        """
        ALTER TABLE disease_detections
        ALTER COLUMN recommendation
        TYPE text
        USING recommendation::text
        """
    )
