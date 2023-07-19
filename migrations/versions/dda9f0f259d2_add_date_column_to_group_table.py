"""Add date column to group table

Revision ID: dda9f0f259d2
Revises: 3084c5954f3a
Create Date: 2023-07-18 12:27:43.626718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dda9f0f259d2'
down_revision = '3084c5954f3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('group', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=False))
        batch_op.drop_column('created_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('group', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DATETIME(), nullable=False))
        batch_op.drop_column('date')

    # ### end Alembic commands ###