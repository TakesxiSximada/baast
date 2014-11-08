"""users

Revision ID: 1b0fbb5d57a
Revises: None
Create Date: 2014-11-04 22:59:51.675696

"""

# revision identifiers, used by Alembic.
revision = '1b0fbb5d57a'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


def upgrade():
    op.create_table(
        'User',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('is_created', sa.TIMESTAMP(), server_default=text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('is_updated', sa.TIMESTAMP(), server_default=text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('is_deleted', sa.TIMESTAMP(), nullable=True),
        sqlite_autoincrement=True,
        )

    op.create_table(
        'UserAttribute',
        sa.Column('user_id', sa.Integer, primary_key=True),
        sa.Column('is_created', sa.TIMESTAMP(), server_default=text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('is_updated', sa.TIMESTAMP(), server_default=text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('name', sa.Unicode, default=''),
        sa.Column('email', sa.Unicode, default=''),
        sa.Column('password', sa.Unicode, default=''),
        sa.Column('first_name', sa.Unicode, default=''),
        sa.Column('middle_name', sa.Unicode, default=''),
        sa.Column('last_name', sa.Unicode, default=''),
        sa.Column('address', sa.Unicode, default=''),
        sa.Column('birth_date', sa.DateTime, nullable=True),
        sa.Column('contact', sa.Unicode, default=''),
        )


def downgrade():
    op.drop_table('UserAttribute')
    op.drop_table('User')
