"""Index Table Config

Revision ID: 3fd2aaf0a53d
Revises: 5ff6e72c50ab
Create Date: 2025-02-01 20:54:18.859586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fd2aaf0a53d'
down_revision: Union[str, None] = '5ff6e72c50ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('idx_config_key_value_is_active', 'config', ['key', 'value', 'is_active'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_config_key_value_is_active', table_name='config')