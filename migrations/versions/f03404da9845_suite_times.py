"""suite times

Revision ID: f03404da9845
Revises: f3bf241a14c0
Create Date: 2022-04-10 22:14:51.439031

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f03404da9845"
down_revision = "f3bf241a14c0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("test_suite", sa.Column("time", sa.Numeric(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("test_suite", "time")
    # ### end Alembic commands ###
