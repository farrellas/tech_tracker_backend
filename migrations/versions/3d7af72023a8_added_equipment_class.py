"""added equipment class

Revision ID: 3d7af72023a8
Revises: 317ba88e39cb
Create Date: 2022-04-24 20:40:38.178673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d7af72023a8'
down_revision = '317ba88e39cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('air_handling_equipment', sa.Column('equipment_class', sa.String(length=50), nullable=False))
    op.add_column('cooling_equipment', sa.Column('equipment_class', sa.String(length=50), nullable=False))
    op.add_column('heating_equipment', sa.Column('equipment_class', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('heating_equipment', 'equipment_class')
    op.drop_column('cooling_equipment', 'equipment_class')
    op.drop_column('air_handling_equipment', 'equipment_class')
    # ### end Alembic commands ###
