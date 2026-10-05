"""Created projetcs table

Revision ID: acbf56362929
Revises: 91f93feb7305
Create Date: 2026-10-04 12:28:16.601366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acbf56362929'
down_revision: Union[str, Sequence[str], None] = '91f93feb7305'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('projects',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('overview', sa.String(), nullable=False),
                    sa.Column('deployment', sa.String(), nullable=False),
                    sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('projects')
    pass
