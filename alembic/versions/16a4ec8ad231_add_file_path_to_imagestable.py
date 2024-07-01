"""Add file_path to ImagesTable

Revision ID: 16a4ec8ad231
Revises: 1cc1d5e23bf0
Create Date: 2024-07-01 13:32:15.959556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16a4ec8ad231'
down_revision: Union[str, None] = '1cc1d5e23bf0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('file_path', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('images', 'file_path')
    # ### end Alembic commands ###