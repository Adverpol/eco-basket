"""rename date cols

Revision ID: 45ffae093328
Revises: 1139f0b4c9e3
Create Date: 2016-05-31 09:08:08.495984

"""

# revision identifiers, used by Alembic.
revision = '45ffae093328'
down_revision = '1139f0b4c9e3'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('close_date_utc', sa.DateTime(), nullable=True))
    op.add_column('orders', sa.Column('delivery_date_utc', sa.DateTime(), nullable=True))
    op.drop_column('orders', 'delivery_date')
    op.drop_column('orders', 'close_date')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('close_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('orders', sa.Column('delivery_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('orders', 'delivery_date_utc')
    op.drop_column('orders', 'close_date_utc')
    ### end Alembic commands ###
