"""Add_foreign_key_to_the_post_table

Revision ID: 6c5aed70e723
Revises: be5a9c49d6aa
Create Date: 2024-11-11 18:33:22.883069

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6c5aed70e723"
down_revision: Union[str, None] = "be5a9c49d6aa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the owner_id column to the posts table
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))

    # Create the foreign key constraint
    op.create_foreign_key(
        "posts_users_fk",  # Constraint name
        "posts",  # Source table
        "users",  # Referenced table
        ["owner_id"],  # Source columns
        ["id"],  # Referenced columns
        ondelete="CASCADE",  # On delete behavior
    )


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", "posts")
    op.drop_column("posts", "owner_id")
