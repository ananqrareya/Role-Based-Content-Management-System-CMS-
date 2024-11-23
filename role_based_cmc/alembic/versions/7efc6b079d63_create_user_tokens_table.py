"""Create user_tokens table

Revision ID: 7efc6b079d63
Revises: 33f8658e5bf4
Create Date: 2024-11-23 19:01:03.886618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7efc6b079d63'
down_revision: Union[str, None] = '33f8658e5bf4'
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
