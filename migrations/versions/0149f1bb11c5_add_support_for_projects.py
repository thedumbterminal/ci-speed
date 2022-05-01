"""Add support for projects.

Revision ID: 0149f1bb11c5
Revises: f03404da9845
Create Date: 2022-05-01 14:58:00.315294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0149f1bb11c5'
down_revision = 'f03404da9845'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('test_run', sa.Column('project_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'test_run', 'project', ['project_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('test_run_project_id_fkey', 'test_run', type_='foreignkey')
    op.drop_column('test_run', 'project_id')
    op.drop_table('project')
    # ### end Alembic commands ###
