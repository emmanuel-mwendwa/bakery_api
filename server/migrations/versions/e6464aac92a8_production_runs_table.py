"""Production Runs Table

Revision ID: e6464aac92a8
Revises: 
Create Date: 2023-10-04 17:25:04.032673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6464aac92a8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.String(length=13), nullable=False),
    sa.Column('product_name', sa.String(length=56), nullable=False),
    sa.Column('product_price', sa.Float(), nullable=False),
    sa.Column('product_description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('product_id')
    )
    op.create_table('production_runs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('flour_kneaded', sa.Integer(), nullable=False),
    sa.Column('oil_used', sa.Float(), nullable=False),
    sa.Column('packets_produced', sa.Float(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('production_runs')
    op.drop_table('products')
    # ### end Alembic commands ###
