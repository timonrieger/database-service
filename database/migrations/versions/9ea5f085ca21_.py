"""empty message

Revision ID: 9ea5f085ca21
Revises: a9ac03c1d07f
Create Date: 2024-11-08 20:35:20.678255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ea5f085ca21'
down_revision = 'a9ac03c1d07f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ressources', schema=None) as batch_op:
        batch_op.drop_column('topic')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ressources', schema=None) as batch_op:
        batch_op.add_column(sa.Column('topic', sa.VARCHAR(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###