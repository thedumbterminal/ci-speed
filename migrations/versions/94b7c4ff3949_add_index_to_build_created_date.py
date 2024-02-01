"""Add index to build created date

Revision ID: 94b7c4ff3949
Revises: 49901dacf799
Create Date: 2023-12-09 23:01:53.742882

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "94b7c4ff3949"
down_revision = "49901dacf799"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("ik_created_at", "build", ["created_at"])


def downgrade():
    op.drop_index("ik_created_at", "build")
