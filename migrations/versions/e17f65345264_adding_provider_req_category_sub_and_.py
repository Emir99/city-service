"""Adding provider - req, category - sub and updated client

Revision ID: e17f65345264
Revises: 
Create Date: 2020-11-14 22:03:43.909779

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e17f65345264'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('icon_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_id'), 'category', ['id'], unique=True)
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=True)
    op.create_table('clients',
    sa.Column('identifier', sa.String(), nullable=False),
    sa.Column('forename', sa.String(length=30), nullable=False),
    sa.Column('surname', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('home_address', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('post_code', sa.String(), nullable=False),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('residency', sa.String(), nullable=False),
    sa.Column('email_confirmation', sa.Boolean(), nullable=False),
    sa.Column('role', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('identifier'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_clients_identifier'), 'clients', ['identifier'], unique=False)
    op.create_table('provider',
    sa.Column('identifier', sa.String(), nullable=False),
    sa.Column('forename', sa.String(length=30), nullable=False),
    sa.Column('surname', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('home_address', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('post_code', sa.String(), nullable=False),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('residency', sa.String(), nullable=False),
    sa.Column('email_confirmation', sa.Boolean(), nullable=False),
    sa.Column('role', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('identifier'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_provider_identifier'), 'provider', ['identifier'], unique=False)
    op.create_table('provider_req',
    sa.Column('identifier', sa.String(), nullable=False),
    sa.Column('forename', sa.String(length=30), nullable=False),
    sa.Column('surname', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('home_address', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('post_code', sa.String(), nullable=False),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('residency', sa.String(), nullable=False),
    sa.Column('email_confirmation', sa.Boolean(), nullable=False),
    sa.Column('role', sa.String(length=10), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('identifier'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_provider_req_identifier'), 'provider_req', ['identifier'], unique=False)
    op.create_table('category_images',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('extension', sa.String(), nullable=False),
    sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_images_extension'), 'category_images', ['extension'], unique=False)
    op.create_index(op.f('ix_category_images_id'), 'category_images', ['id'], unique=True)
    op.create_index(op.f('ix_category_images_path'), 'category_images', ['path'], unique=True)
    op.create_table('client_contacts',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('client_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.identifier'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_client_contacts_id'), 'client_contacts', ['id'], unique=True)
    op.create_table('client_images',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('extension', sa.String(), nullable=False),
    sa.Column('client_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.identifier'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_client_images_extension'), 'client_images', ['extension'], unique=False)
    op.create_index(op.f('ix_client_images_id'), 'client_images', ['id'], unique=True)
    op.create_index(op.f('ix_client_images_path'), 'client_images', ['path'], unique=True)
    op.create_table('client_languages',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('client_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.identifier'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_client_languages_id'), 'client_languages', ['id'], unique=True)
    op.create_table('provider_category',
    sa.Column('provider_id', sa.String(), nullable=True),
    sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.identifier'], )
    )
    op.create_table('provider_contacts',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('provider_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.identifier'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_contacts_id'), 'provider_contacts', ['id'], unique=True)
    op.create_table('provider_contacts_req',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('provider_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['provider_req.identifier'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_contacts_req_id'), 'provider_contacts_req', ['id'], unique=True)
    op.create_table('provider_images',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('extension', sa.String(), nullable=False),
    sa.Column('provider_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.identifier'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_images_extension'), 'provider_images', ['extension'], unique=False)
    op.create_index(op.f('ix_provider_images_id'), 'provider_images', ['id'], unique=True)
    op.create_index(op.f('ix_provider_images_path'), 'provider_images', ['path'], unique=True)
    op.create_table('provider_images_req',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('extension', sa.String(), nullable=False),
    sa.Column('provider_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['provider_req.identifier'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_images_req_extension'), 'provider_images_req', ['extension'], unique=False)
    op.create_index(op.f('ix_provider_images_req_id'), 'provider_images_req', ['id'], unique=True)
    op.create_index(op.f('ix_provider_images_req_path'), 'provider_images_req', ['path'], unique=True)
    op.create_table('provider_languages',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('provider_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.identifier'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_languages_id'), 'provider_languages', ['id'], unique=True)
    op.create_table('provider_languages_req',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('provider_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['provider_req.identifier'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_languages_req_id'), 'provider_languages_req', ['id'], unique=True)
    op.create_table('provider_personal',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('provider_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.identifier'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_personal_id'), 'provider_personal', ['id'], unique=True)
    op.create_table('provider_req_category',
    sa.Column('provider_req_id', sa.String(), nullable=True),
    sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['provider_req_id'], ['provider_req.identifier'], )
    )
    op.create_table('subcategory',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('icon_name', sa.String(), nullable=True),
    sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subcategory_id'), 'subcategory', ['id'], unique=True)
    op.create_index(op.f('ix_subcategory_name'), 'subcategory', ['name'], unique=True)
    op.create_table('provider_req_subcategory',
    sa.Column('provider_req_id', sa.String(), nullable=True),
    sa.Column('subcategory_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['provider_req_id'], ['provider_req.identifier'], ),
    sa.ForeignKeyConstraint(['subcategory_id'], ['subcategory.id'], )
    )
    op.create_table('provider_subcategory',
    sa.Column('provider_id', sa.String(), nullable=True),
    sa.Column('subcategory_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.identifier'], ),
    sa.ForeignKeyConstraint(['subcategory_id'], ['subcategory.id'], )
    )
    op.create_table('subcategory_images',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('extension', sa.String(), nullable=False),
    sa.Column('subcategory_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['subcategory_id'], ['subcategory.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subcategory_images_extension'), 'subcategory_images', ['extension'], unique=False)
    op.create_index(op.f('ix_subcategory_images_id'), 'subcategory_images', ['id'], unique=True)
    op.create_index(op.f('ix_subcategory_images_path'), 'subcategory_images', ['path'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_subcategory_images_path'), table_name='subcategory_images')
    op.drop_index(op.f('ix_subcategory_images_id'), table_name='subcategory_images')
    op.drop_index(op.f('ix_subcategory_images_extension'), table_name='subcategory_images')
    op.drop_table('subcategory_images')
    op.drop_table('provider_subcategory')
    op.drop_table('provider_req_subcategory')
    op.drop_index(op.f('ix_subcategory_name'), table_name='subcategory')
    op.drop_index(op.f('ix_subcategory_id'), table_name='subcategory')
    op.drop_table('subcategory')
    op.drop_table('provider_req_category')
    op.drop_index(op.f('ix_provider_personal_id'), table_name='provider_personal')
    op.drop_table('provider_personal')
    op.drop_index(op.f('ix_provider_languages_req_id'), table_name='provider_languages_req')
    op.drop_table('provider_languages_req')
    op.drop_index(op.f('ix_provider_languages_id'), table_name='provider_languages')
    op.drop_table('provider_languages')
    op.drop_index(op.f('ix_provider_images_req_path'), table_name='provider_images_req')
    op.drop_index(op.f('ix_provider_images_req_id'), table_name='provider_images_req')
    op.drop_index(op.f('ix_provider_images_req_extension'), table_name='provider_images_req')
    op.drop_table('provider_images_req')
    op.drop_index(op.f('ix_provider_images_path'), table_name='provider_images')
    op.drop_index(op.f('ix_provider_images_id'), table_name='provider_images')
    op.drop_index(op.f('ix_provider_images_extension'), table_name='provider_images')
    op.drop_table('provider_images')
    op.drop_index(op.f('ix_provider_contacts_req_id'), table_name='provider_contacts_req')
    op.drop_table('provider_contacts_req')
    op.drop_index(op.f('ix_provider_contacts_id'), table_name='provider_contacts')
    op.drop_table('provider_contacts')
    op.drop_table('provider_category')
    op.drop_index(op.f('ix_client_languages_id'), table_name='client_languages')
    op.drop_table('client_languages')
    op.drop_index(op.f('ix_client_images_path'), table_name='client_images')
    op.drop_index(op.f('ix_client_images_id'), table_name='client_images')
    op.drop_index(op.f('ix_client_images_extension'), table_name='client_images')
    op.drop_table('client_images')
    op.drop_index(op.f('ix_client_contacts_id'), table_name='client_contacts')
    op.drop_table('client_contacts')
    op.drop_index(op.f('ix_category_images_path'), table_name='category_images')
    op.drop_index(op.f('ix_category_images_id'), table_name='category_images')
    op.drop_index(op.f('ix_category_images_extension'), table_name='category_images')
    op.drop_table('category_images')
    op.drop_index(op.f('ix_provider_req_identifier'), table_name='provider_req')
    op.drop_table('provider_req')
    op.drop_index(op.f('ix_provider_identifier'), table_name='provider')
    op.drop_table('provider')
    op.drop_index(op.f('ix_clients_identifier'), table_name='clients')
    op.drop_table('clients')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_index(op.f('ix_category_id'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###
