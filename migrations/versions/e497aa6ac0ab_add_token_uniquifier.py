"""Add token uniquifier

Revision ID: e497aa6ac0ab
Revises: 4f6214cbae7f
Create Date: 2022-05-12 21:34:57.730951

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e497aa6ac0ab"
down_revision = "4f6214cbae7f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("fs_uniquifier", sa.String(length=255), nullable=False)
    )
    op.create_unique_constraint(None, "user", ["fs_uniquifier"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user", type_="unique")
    op.drop_column("user", "fs_uniquifier")
    # ### end Alembic commands ###
