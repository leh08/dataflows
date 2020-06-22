"""Create tables

Revision ID: 67ee9d88e46d
Revises: 
Create Date: 2020-06-22 16:46:02.568652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67ee9d88e46d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('authorizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('credential', sa.JSON(), nullable=True),
    sa.Column('source_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['source_id'], ['sources.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('confirmations',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('expire_at', sa.Integer(), nullable=False),
    sa.Column('confirmed', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('flows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('report', sa.String(), nullable=False),
    sa.Column('profile', sa.String(), nullable=True),
    sa.Column('parser_name', sa.String(), nullable=True),
    sa.Column('store_name', sa.String(), nullable=True),
    sa.Column('is_model', sa.Boolean(), nullable=True),
    sa.Column('schema', sa.String(), nullable=True),
    sa.Column('load_mode', sa.String(), nullable=True),
    sa.Column('frequency', sa.String(), nullable=True),
    sa.Column('day_unit', sa.String(), nullable=True),
    sa.Column('time_unit', sa.Integer(), nullable=True),
    sa.Column('sql_script', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('source_name', sa.String(), nullable=True),
    sa.Column('authorization_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['authorization_id'], ['authorizations.id'], ),
    sa.ForeignKeyConstraint(['source_name'], ['sources.name'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('file', sa.String(), nullable=True),
    sa.Column('flow_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['flow_id'], ['flows.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('logs')
    op.drop_table('flows')
    op.drop_table('confirmations')
    op.drop_table('authorizations')
    op.drop_table('users')
    op.drop_table('sources')
    # ### end Alembic commands ###