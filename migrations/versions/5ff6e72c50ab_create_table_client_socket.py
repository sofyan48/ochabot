"""Create Table Client Socket

Revision ID: 5ff6e72c50ab
Revises: 31b92c51b921
Create Date: 2025-02-01 20:54:04.589683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ff6e72c50ab'
down_revision: Union[str, None] = '31b92c51b921'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'client_sockets',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), index=True),
        sa.Column('secret', sa.String()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('client_sockets')