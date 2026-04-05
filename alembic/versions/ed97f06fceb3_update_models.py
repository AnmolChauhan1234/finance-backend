"""update models

Revision ID: ed97f06fceb3
Revises: f6fec91404ca
Create Date: 2026-04-05 08:19:06.938885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ed97f06fceb3'
down_revision: Union[str, Sequence[str], None] = 'f6fec91404ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # 🔥 1. Create new ENUM FIRST
    record_type_enum = postgresql.ENUM(
        'INCOME', 'EXPENSE',
        name='record_type_enum'
    )
    record_type_enum.create(op.get_bind(), checkfirst=True)

    role_enum = postgresql.ENUM(
        'VIEWER', 'ANALYST', 'ADMIN',
        name='role_enum'
    )
    role_enum.create(op.get_bind(), checkfirst=True)

    # 🔥 2. Add new columns
    op.add_column('financial_records', sa.Column('created_at', sa.DateTime(), nullable=True))

    # 🔥 3. Alter ENUM column
    op.alter_column(
        'financial_records',
        'type',
        existing_type=postgresql.ENUM('INCOME', 'EXPENSE', name='recordtype'),
        type_=record_type_enum,
        existing_nullable=False,
        postgresql_using="type::text::record_type_enum"  # 🔥 CRITICAL FIX
    )

    op.alter_column(
        'financial_records',
        'user_id',
        existing_type=sa.INTEGER(),
        nullable=False
    )

    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), nullable=True))

    op.alter_column(
        'users',
        'role',
        existing_type=postgresql.ENUM('VIEWER', 'ANALYST', 'ADMIN', name='role'),
        type_=role_enum,
        existing_nullable=False,
        postgresql_using="role::text::role_enum"  # 🔥 IMPORTANT
    )

    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)

    # 🔥 4. Optional: drop old enums
    op.execute("DROP TYPE IF EXISTS recordtype")
    op.execute("DROP TYPE IF EXISTS role")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(op.f('ix_users_role'), table_name='users')

    # recreate old enums
    old_record_enum = postgresql.ENUM(
        'INCOME', 'EXPENSE',
        name='recordtype'
    )
    old_record_enum.create(op.get_bind(), checkfirst=True)

    old_role_enum = postgresql.ENUM(
        'VIEWER', 'ANALYST', 'ADMIN',
        name='role'
    )
    old_role_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        'users',
        'role',
        existing_type=sa.Enum('VIEWER', 'ANALYST', 'ADMIN', name='role_enum'),
        type_=old_role_enum,
        existing_nullable=False
    )

    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')

    op.alter_column(
        'financial_records',
        'user_id',
        existing_type=sa.INTEGER(),
        nullable=True
    )

    op.alter_column(
        'financial_records',
        'type',
        existing_type=sa.Enum('INCOME', 'EXPENSE', name='record_type_enum'),
        type_=old_record_enum,
        existing_nullable=False
    )

    op.drop_column('financial_records', 'created_at')

    # cleanup new enums
    op.execute("DROP TYPE IF EXISTS record_type_enum")
    op.execute("DROP TYPE IF EXISTS role_enum")
    # ### end Alembic commands ###
