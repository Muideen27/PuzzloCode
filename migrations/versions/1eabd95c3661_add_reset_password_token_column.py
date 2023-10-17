"""Add reset_password_token column

Revision ID: 1eabd95c3661
Revises: 3d512104b8fe
Create Date: 2023-10-13 21:32:02.685513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1eabd95c3661'
down_revision = '3d512104b8fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reset_password_token', sa.String(length=100), nullable=True))
        batch_op.create_unique_constraint(None, ['reset_password_token'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('reset_password_token')

    # ### end Alembic commands ###
