"""Create Table Ingest Historie

Revision ID: 34e25b210fc0
Revises: 8014b8ae1b83
Create Date: 2025-02-03 15:31:06.049664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34e25b210fc0'
down_revision: Union[str, None] = '8014b8ae1b83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ingest_documents',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('ingest_code', sa.String(length=200), nullable=False, unique=True),
        sa.Column('file_path', sa.String(length=200), nullable=False),
        sa.Column('overlap', sa.Integer(), nullable=False),
        sa.Column('chunk', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP'))
    )

def downgrade() -> None:
    op.drop_table('ingest_documents')