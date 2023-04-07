"""

Revision ID: 76b4148b875a
Revises: 087318aa89b0
Create Date: 2023-02-16 23:04:12.914305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76b4148b875a'
down_revision = '087318aa89b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_review_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'productreviews', ['product_review_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('product_review_id')

    # ### end Alembic commands ###
