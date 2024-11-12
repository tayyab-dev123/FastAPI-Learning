"""add content column in posts table

Revision ID: bd02c2263dd7
Revises: 52a2d0fbc917
Create Date: 2024-11-11 17:56:50.490919

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bd02c2263dd7"
down_revision: Union[str, None] = "52a2d0fbc917"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=True))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
