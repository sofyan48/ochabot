"""Create Default User

Revision ID: 5842f4c904f6
Revises: 8e0654346df6
Create Date: 2025-02-02 21:37:03.547137

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5842f4c904f6'
down_revision: Union[str, None] = '8e0654346df6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        """
        INSERT INTO users (id, name, email, username, password, is_active)
        VALUES 
        (1, 'admin', 'admin@iank.me', 'admin', '$2b$12$T6ys0.xYxh/2vpyw6HFFvu5HhUUejNE9QZ3n.mnbml7UiqpPoz7Ni', true)
        """
    )

def downgrade():
    op.execute(
        """
        DELETE FROM users WHERE id = 1
        """
    )