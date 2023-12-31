"""Production runs cost and expected profits

Revision ID: 4a7ed5f1e953
Revises: ad3470c516ae
Create Date: 2023-10-12 14:40:50.323942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a7ed5f1e953'
down_revision = 'ad3470c516ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('production_runs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('run_cost', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('expected_profit', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('production_runs', schema=None) as batch_op:
        batch_op.drop_column('expected_profit')
        batch_op.drop_column('run_cost')

    # ### end Alembic commands ###
