"""Add support for builds

Revision ID: ad19c9990883
Revises: e497aa6ac0ab
Create Date: 2022-05-17 18:06:44.156791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ad19c9990883"
down_revision = "e497aa6ac0ab"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "build",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("test_run", sa.Column("build_id", sa.Integer(), nullable=False))
    op.drop_constraint("test_run_project_id_fkey", "test_run", type_="foreignkey")
    op.create_foreign_key(None, "test_run", "build", ["build_id"], ["id"])
    op.drop_column("test_run", "project_id")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "test_run",
        sa.Column("project_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "test_run", type_="foreignkey")
    op.create_foreign_key(
        "test_run_project_id_fkey", "test_run", "project", ["project_id"], ["id"]
    )
    op.drop_column("test_run", "build_id")
    op.drop_table("build")
    # ### end Alembic commands ###
