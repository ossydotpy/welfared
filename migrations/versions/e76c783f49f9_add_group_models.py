"""add group models

Revision ID: e76c783f49f9
Revises: 462238aa4e1e
Create Date: 2025-06-04 10:56:01.513781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e76c783f49f9'
down_revision = '462238aa4e1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('logo', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user._id'], ),
    sa.PrimaryKeyConstraint('_id')
    )
    op.create_table('group_member',
    sa.Column('_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group._id'], ),
    sa.PrimaryKeyConstraint('_id')
    )
    op.create_table('welfare_payment',
    sa.Column('_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('frequency', sa.String(), nullable=False),
    sa.Column('last_paid_date', sa.Date(), nullable=True),
    sa.Column('next_due_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group._id'], ),
    sa.PrimaryKeyConstraint('_id')
    )
    op.create_table('welfare_payment_transaction',
    sa.Column('_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('welfare_payment_id', sa.Integer(), nullable=False),
    sa.Column('group_member_id', sa.Integer(), nullable=False),
    sa.Column('amount_paid', sa.Float(), nullable=False),
    sa.Column('payment_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['group_member_id'], ['group_member._id'], ),
    sa.ForeignKeyConstraint(['welfare_payment_id'], ['welfare_payment._id'], ),
    sa.PrimaryKeyConstraint('_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('welfare_payment_transaction')
    op.drop_table('welfare_payment')
    op.drop_table('group_member')
    op.drop_table('group')
    # ### end Alembic commands ###
