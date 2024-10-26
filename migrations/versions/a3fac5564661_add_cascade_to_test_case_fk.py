"""add cascade to test_case fk

Revision ID: a3fac5564661
Revises: 83ffe031774f
Create Date: 2024-10-26 16:47:19.685554

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a3fac5564661"
down_revision = "83ffe031774f"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("test_suite", schema=None) as batch_op:
        batch_op.drop_constraint("test_suite_test_run_id_fkey", type_="foreignkey")
        batch_op.create_foreign_key(
            None, "test_run", ["test_run_id"], ["id"], ondelete="CASCADE"
        )


def downgrade():
    with op.batch_alter_table("test_suite", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.create_foreign_key(
            "test_suite_test_run_id_fkey", "test_run", ["test_run_id"], ["id"]
        )
