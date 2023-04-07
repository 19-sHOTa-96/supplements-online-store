"""

Revision ID: 087318aa89b0
Revises: aa5a65c91cd7
Create Date: 2023-02-16 22:44:08.898465

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '087318aa89b0'
down_revision = 'aa5a65c91cd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('productreviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('review', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('productdetails', schema=None) as batch_op:
        batch_op.drop_column('product_brand')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('review_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'productreviews', ['review_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('review_id')

    with op.batch_alter_table('productdetails', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_brand', mysql.VARCHAR(length=64), nullable=True))

    op.drop_table('productreviews')
    # ### end Alembic commands ###
