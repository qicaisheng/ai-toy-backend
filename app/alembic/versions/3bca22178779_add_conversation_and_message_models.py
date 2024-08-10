"""add conversation and message models

Revision ID: 3bca22178779
Revises: 1a31ce608336
Create Date: 2024-08-10 23:05:03.849779

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '3bca22178779'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conversation',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('user_id', sa.UUID(), nullable=False),
                    sa.Column('created_time', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('message',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('conversation_id', sa.UUID(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('audio_id', sa.String(), nullable=True),
                    sa.Column('author', sa.JSON(), nullable=False),
                    sa.Column('parent_id', sa.UUID(), nullable=True),
                    sa.Column('created_time', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    op.drop_table('conversation')
    # ### end Alembic commands ###
