"""update table ingest docs 

Revision ID: 5870acc8a775
Revises: 34e25b210fc0
Create Date: 2025-02-04 21:17:14.984160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5870acc8a775'
down_revision: Union[str, None] = '34e25b210fc0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('ingest_documents', sa.Column('is_build', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade() -> None:
    op.drop_column('ingest_documents', 'is_build')