"""empty message

Revision ID: 427c4fc56fd5
Revises: 8b2343992c45
Create Date: 2024-11-04 22:02:42.881434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '427c4fc56fd5'
down_revision = '8b2343992c45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('top_movies', schema=None) as batch_op:
        batch_op.drop_column('ranking')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('top_movies', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ranking', sa.INTEGER(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
