"""Issues table created

Revision ID: f630329a38cd
Revises: acbf56362929
Create Date: 2026-10-05 09:47:32.726819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f630329a38cd'
down_revision: Union[str, Sequence[str], None] = 'acbf56362929'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('issues',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('label', sa.String(), nullable=False),
                    sa.Column('priority', sa.Integer(), nullable=False),
                    sa.Column('status', sa.String(), nullable=False),
                    sa.Column('assignee', sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
                    sa.Column('project_id', sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('issues')
    pass
