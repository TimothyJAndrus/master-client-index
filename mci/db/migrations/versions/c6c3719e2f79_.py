"""Remove Current Status Table and Relationship.

Revision ID: c6c3719e2f79
Revises: e1bdd0f39e93
Create Date: 2019-03-27 12:27:33.244748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6c3719e2f79'
down_revision = 'e1bdd0f39e93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('current_status')
    op.drop_table('individual_current_status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('individual_current_status',
                    sa.Column('mci_id', sa.VARCHAR(length=40),
                              autoincrement=False, nullable=False),
                    sa.Column('current_status_id', sa.INTEGER(),
                              autoincrement=False, nullable=False),
                    sa.ForeignKeyConstraint(['current_status_id'], [
                        'current_status.id'], name='individual_current_status_current_status_id_fkey'),
                    sa.ForeignKeyConstraint(['mci_id'], [
                        'individual.mci_id'], name='individual_current_status_mci_id_fkey', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint(
                        'mci_id', 'current_status_id', name='individual_current_status_pkey')
                    )
    op.create_table('current_status',
                    sa.Column('id', sa.INTEGER(),
                              autoincrement=True, nullable=False),
                    sa.Column('current_status', sa.VARCHAR(),
                              autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='current_status_pkey')
                    )
    # ### end Alembic commands ###
