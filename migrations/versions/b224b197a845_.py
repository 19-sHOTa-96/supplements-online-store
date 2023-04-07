"""

Revision ID: b224b197a845
Revises: b6f7b57de744
Create Date: 2023-02-13 18:45:32.183589

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b224b197a845'
down_revision = 'b6f7b57de744'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('wishlist_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('users_ibfk_4', type_='foreignkey')
        batch_op.create_foreign_key(None, 'wishlists', ['wishlist_id'], ['id'])
        batch_op.drop_column('wishlist')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('wishlist', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('users_ibfk_4', 'wishlists', ['wishlist'], ['id'])
        batch_op.drop_column('wishlist_id')

    # ### end Alembic commands ###
