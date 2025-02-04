"""update table ingest docs

Revision ID: fe5fb63d8d97
Revises: 5870acc8a775
Create Date: 2025-02-04 21:41:02.899707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe5fb63d8d97'
down_revision: Union[str, None] = '5870acc8a775'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('ingest_documents', sa.Column('collection', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('ingest_documents', 'collection')