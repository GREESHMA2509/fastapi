"""add users table

Revision ID: 3073922953fa
Revises: 727d9a24809a
Create Date: 2025-09-07 16:50:08.188681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3073922953fa'
down_revision: Union[str, Sequence[str], None] = '727d9a24809a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
        sa.Column('id',sa.Integer(),nullable=False),
        sa.Column('enail',sa.String(),nullable=False),
        sa.Column('passowrd',sa.String(),nullable=False),
        sa.Column('created_At',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
        sa.primaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
