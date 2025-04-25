"""add cascade to test_runs fk

Revision ID: 83ffe031774f
Revises: 4dfa97c59993
Create Date: 2024-10-23 19:41:49.415694

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "83ffe031774f"
down_revision = "4dfa97c59993"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("test_run_build_id_fkey", "test_run", type_="foreignkey")
    op.create_foreign_key(
        None,
        "test_run",
        "build",
        ["build_id"],
        ["id"],
        ondelete="CASCADE",
        onupdate="CASCADE",
    )


def downgrade():
    op.drop_constraint("test_run_build_id_fkey", "test_run", type_="foreignkey")
    op.create_foreign_key(None, "test_run", "build", ["build_id"], ["id"])
