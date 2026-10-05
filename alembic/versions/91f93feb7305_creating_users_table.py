"""creating users table

Revision ID: 91f93feb7305
Revises: 
Create Date: 2026-10-04 09:38:55.629385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91f93feb7305'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()'))
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass