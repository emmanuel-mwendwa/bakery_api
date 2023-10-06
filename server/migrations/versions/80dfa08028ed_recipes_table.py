"""recipes table

Revision ID: 80dfa08028ed
Revises: 10795d1edf2d
Create Date: 2023-10-06 09:35:51.571095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80dfa08028ed'
down_revision = '10795d1edf2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('yield_amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipe_ingredients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('ingredient_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('unit_of_measurement', sa.String(length=12), nullable=True),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe_ingredients')
    op.drop_table('recipes')
    # ### end Alembic commands ###