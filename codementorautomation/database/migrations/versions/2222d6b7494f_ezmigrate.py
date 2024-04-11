"""ezmigrate

Revision ID: 2222d6b7494f
Revises: 4928cf8d42b3
Create Date: 2023-10-11 21:41:54.699244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2222d6b7494f'
down_revision: Union[str, None] = '4928cf8d42b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expertise', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_whitelisted', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expertise', schema=None) as batch_op:
        batch_op.drop_column('is_whitelisted')

    # ### end Alembic commands ###
