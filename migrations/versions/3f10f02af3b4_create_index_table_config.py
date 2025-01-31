"""Create Index Table Config

Revision ID: 3f10f02af3b4
Revises: fbfc4531b29e
Create Date: 2025-01-31 08:34:12.809274

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f10f02af3b4'
down_revision: Union[str, None] = 'fbfc4531b29e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('idx_config_key_value_is_active', 'config', ['key', 'value', 'is_active'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_config_key_value_is_active', table_name='config')
