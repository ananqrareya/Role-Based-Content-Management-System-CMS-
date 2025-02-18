"""Create user_token table

Revision ID: 7bd525a3c2ae
Revises: d3f7d6258694
Create Date: 2025-02-17 01:28:54.516566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7bd525a3c2ae'
down_revision: Union[str, None] = 'd3f7d6258694'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_tokens',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('token', sa.Text(), nullable=False),
    sa.Column('issued_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('expires_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_tokens')
    # ### end Alembic commands ###
