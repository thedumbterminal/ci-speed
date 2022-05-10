"""Supporting auth

Revision ID: 4f6214cbae7f
Revises: 0149f1bb11c5
Create Date: 2022-05-08 23:48:39.426711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f6214cbae7f'
down_revision = '0149f1bb11c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('flask_dance_oauth',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('token', sa.JSON(), nullable=False),
    sa.Column('provider_user_id', sa.String(length=256), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('provider_user_id')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.drop_constraint('test_case_test_suite_id_fkey', 'test_case', type_='foreignkey')
    op.create_foreign_key(None, 'test_case', 'test_suite', ['test_suite_id'], ['id'])
    op.drop_constraint('test_run_project_id_fkey', 'test_run', type_='foreignkey')
    op.create_foreign_key(None, 'test_run', 'project', ['project_id'], ['id'])
    op.drop_constraint('test_suite_test_run_id_fkey', 'test_suite', type_='foreignkey')
    op.create_foreign_key(None, 'test_suite', 'test_run', ['test_run_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'test_suite', type_='foreignkey')
    op.create_foreign_key('test_suite_test_run_id_fkey', 'test_suite', 'test_run', ['test_run_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint(None, 'test_run', type_='foreignkey')
    op.create_foreign_key('test_run_project_id_fkey', 'test_run', 'project', ['project_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint(None, 'test_case', type_='foreignkey')
    op.create_foreign_key('test_case_test_suite_id_fkey', 'test_case', 'test_suite', ['test_suite_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_table('roles_users')
    op.drop_table('flask_dance_oauth')
    op.drop_table('user')
    op.drop_table('role')
    # ### end Alembic commands ###
