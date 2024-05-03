"""add filename to test run

Revision ID: 2b0de42ea2ad
Revises: 94b7c4ff3949
Create Date: 2024-05-04 00:05:19.271795

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2b0de42ea2ad"
down_revision = "94b7c4ff3949"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("test_run", schema=None) as batch_op:
        batch_op.add_column(sa.Column("file_name", sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table("test_run", schema=None) as batch_op:
        batch_op.drop_column("file_name")
