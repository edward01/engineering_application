"""feature_requests table

Revision ID: 79e9d8e57a9d
Revises: 
Create Date: 2018-12-07 11:09:03.182415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79e9d8e57a9d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feature_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('target_date', sa.Date(), nullable=False),
    sa.Column('client', sa.String(length=20), nullable=False),
    sa.Column('product_area', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feature_request_client'), 'feature_request', ['client'], unique=False)
    op.create_index(op.f('ix_feature_request_product_area'), 'feature_request', ['product_area'], unique=False)
    op.create_index(op.f('ix_feature_request_title'), 'feature_request', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_feature_request_title'), table_name='feature_request')
    op.drop_index(op.f('ix_feature_request_product_area'), table_name='feature_request')
    op.drop_index(op.f('ix_feature_request_client'), table_name='feature_request')
    op.drop_table('feature_request')
    # ### end Alembic commands ###
