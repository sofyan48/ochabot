"""Create Table Client

Revision ID: 8014b8ae1b83
Revises: 5842f4c904f6
Create Date: 2025-02-03 10:45:36.363712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8014b8ae1b83'
down_revision: Union[str, None] = '5842f4c904f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(length=200), nullable=False, unique=True),
        sa.Column('api_key', sa.String(length=200), nullable=False, unique=True),
        sa.Column('secret_key', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP'))
    )

def downgrade() -> None:
    op.drop_table('clients')
