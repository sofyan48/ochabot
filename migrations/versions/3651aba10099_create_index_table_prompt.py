"""Create Index Table prompt

Revision ID: 3651aba10099
Revises: 3fd2aaf0a53d
Create Date: 2025-02-02 09:05:44.388349

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3651aba10099'
down_revision: Union[str, None] = '3fd2aaf0a53d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'prompts',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('prompt', sa.String(100), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP'))
    )


def downgrade() -> None:
    op.drop_table('prompts')