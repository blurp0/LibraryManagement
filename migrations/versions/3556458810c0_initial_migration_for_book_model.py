"""Initial migration for Book model

Revision ID: 3556458810c0
Revises: 
Create Date: 2024-11-25 14:42:03.617246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3556458810c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('author', sa.String(length=255), nullable=False),
    sa.Column('publication_year', sa.Integer(), nullable=True),
    sa.Column('isbn', sa.String(length=13), nullable=True),
    sa.Column('copies_available', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('isbn')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    # ### end Alembic commands ###
