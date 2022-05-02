"""Initial migration.

Revision ID: f3bf241a14c0
Revises: 
Create Date: 2022-04-10 21:38:36.739491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3bf241a14c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test_run',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('test_suite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('test_run_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['test_run_id'], ['test_run.id'], ondelete='CASCADE', onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('test_case',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('time', sa.Numeric(), nullable=True),
    sa.Column('test_suite_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['test_suite_id'], ['test_suite.id'], ondelete='CASCADE', onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test_case')
    op.drop_table('test_suite')
    op.drop_table('test_run')
    # ### end Alembic commands ###