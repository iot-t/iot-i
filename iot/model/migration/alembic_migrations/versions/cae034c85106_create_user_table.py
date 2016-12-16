"""create user table

Revision ID: cae034c85106
Revises: 
Create Date: 2016-12-14 10:10:01.051407

"""

# revision identifiers, used by Alembic.
revision = 'cae034c85106'
down_revision = None
branch_labels = None
depends_on = None

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(20), nullable=False),
        sa.Column('passwd', sa.String(50), nullable=False),
        sa.Column('salt', sa.String(50), nullable=False),
        sa.Column('email', sa.String(50), nullable=False),
        sa.Column('create_at', sa.DateTime, default=datetime.datetime.utcnow),
        sa.Column('actived', sa.Boolean, default=False)
    )

def downgrade():
    op.drop_table('users')
