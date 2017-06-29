"""empty message

Revision ID: 935a51929dab
Revises: 4635d97427d3
Create Date: 2017-06-17 12:13:29.055199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '935a51929dab'
down_revision = '4635d97427d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_one_instal_ix', 'installation', ['app_id', 'device_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_one_instal_ix', 'installation', type_='unique')
    # ### end Alembic commands ###