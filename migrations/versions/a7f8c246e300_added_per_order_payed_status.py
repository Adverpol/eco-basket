"""Added per-order payed status

Revision ID: a7f8c246e300
Revises: 45ffae093328
Create Date: 2016-06-08 14:41:26.472430

"""

# revision identifiers, used by Alembic.
revision = 'a7f8c246e300'
down_revision = '45ffae093328'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_items', sa.Column('payed', sa.Boolean(), server_default='0', nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_items', 'payed')
    ### end Alembic commands ###
