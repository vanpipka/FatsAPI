"""empty message

Revision ID: fb8cb2849a72
Revises: 205fb8347b73
Create Date: 2023-03-19 14:00:16.443622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb8cb2849a72'
down_revision = '205fb8347b73'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vessels', sa.Column('marine_traffic_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vessels', 'marine_traffic_id')
    # ### end Alembic commands ###
