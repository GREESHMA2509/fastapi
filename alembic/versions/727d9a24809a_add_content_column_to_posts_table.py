"""add content column to posts table

Revision ID: 727d9a24809a
Revises: e16133e7704a
Create Date: 2025-09-07 16:44:34.490090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '727d9a24809a'
down_revision: Union[str, Sequence[str], None] = 'e16133e7704a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
