"""empty message

Revision ID: 752996f91722
Revises: 4b87e5d974d9
Create Date: 2024-12-01 17:34:11.224611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '752996f91722'
down_revision = '4b87e5d974d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('author', sa.String(length=100), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('confession')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('confession',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=255), nullable=False),
    sa.Column('confession', sa.TEXT(), nullable=False),
    sa.Column('author', sa.VARCHAR(length=100), nullable=False),
    sa.Column('date_created', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('post')
    # ### end Alembic commands ###
