"""Allow users to own projects

Revision ID: e33c1dca09c2
Revises: f4a1d9c33387
Create Date: 2022-05-19 18:07:18.507960

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e33c1dca09c2"
down_revision = "f4a1d9c33387"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("project", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(None, "project", "user", ["user_id"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "project", type_="foreignkey")
    op.drop_column("project", "user_id")
    # ### end Alembic commands ###
