"""fix topic edge foreign key constraints for cascade delete

Revision ID: f0cc51e128a5
Revises: d17a09735277
Create Date: 2025-09-19 01:04:37.504827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0cc51e128a5'
down_revision: Union[str, Sequence[str], None] = 'd17a09735277'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop existing foreign key constraints
    op.drop_constraint('topic_edges_source_fkey', 'topic_edges', type_='foreignkey')
    op.drop_constraint('topic_edges_target_fkey', 'topic_edges', type_='foreignkey')

    # Add new foreign key constraints with CASCADE DELETE
    op.create_foreign_key('topic_edges_source_fkey', 'topic_edges', 'topics', ['source'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('topic_edges_target_fkey', 'topic_edges', 'topics', ['target'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    # Drop CASCADE foreign key constraints
    op.drop_constraint('topic_edges_source_fkey', 'topic_edges', type_='foreignkey')
    op.drop_constraint('topic_edges_target_fkey', 'topic_edges', type_='foreignkey')

    # Add back original foreign key constraints without CASCADE
    op.create_foreign_key('topic_edges_source_fkey', 'topic_edges', 'topics', ['source'], ['id'])
    op.create_foreign_key('topic_edges_target_fkey', 'topic_edges', 'topics', ['target'], ['id'])
