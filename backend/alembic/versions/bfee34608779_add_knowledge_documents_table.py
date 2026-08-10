"""add knowledge_documents table

Revision ID: bfee34608779
Revises: 9529a10ecf85
Create Date: 2026-08-06 19:46:26.890232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = 'bfee34608779'
down_revision: Union[str, Sequence[str], None] = '9529a10ecf85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "knowledge_documents",
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("chunk_text", sa.Text(), nullable=False),
        sa.Column("embedding", Vector(384), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_knowledge_documents_title"), "knowledge_documents", ["title"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_knowledge_documents_title"), table_name="knowledge_documents")
    op.drop_table("knowledge_documents")
