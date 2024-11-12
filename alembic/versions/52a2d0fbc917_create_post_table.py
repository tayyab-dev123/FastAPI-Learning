"""create_post_table

Revision ID: 52a2d0fbc917
Revises: 
Create Date: 2024-11-11 17:47:17.431981

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "52a2d0fbc917"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, nullable=True, primary_key=True),
        sa.Column("title", sa.String, nullable=True),
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
