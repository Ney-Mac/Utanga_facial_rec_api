"""Aumentar tamanho id_turma e id_cadeira para 20

Revision ID: dd985384c003
Revises: 
Create Date: 2025-05-29 17:43:13.715497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd985384c003'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    """Upgrade schema."""
    op.alter_column('ControleAcesso', 'id_turma',
                    existing_type=sa.String(length=10),
                    type_=sa.String(length=20),
                    existing_nullable=False)
    op.alter_column('ControleAcesso', 'id_cadeira',
                    existing_type=sa.String(length=10),
                    type_=sa.String(length=20),
                    existing_nullable=False)

    op.alter_column('SolicitacaoAcessoEspecial', 'id_turma',
                    existing_type=sa.String(length=10),
                    type_=sa.String(length=20),
                    existing_nullable=False)
    op.alter_column('SolicitacaoAcessoEspecial', 'id_cadeira',
                    existing_type=sa.String(length=10),
                    type_=sa.String(length=20),
                    existing_nullable=False)

def downgrade():
    """Downgrade schema."""
    op.alter_column('ControleAcesso', 'id_turma',
                    existing_type=sa.String(length=20),
                    type_=sa.String(length=10),
                    existing_nullable=False)
    op.alter_column('ControleAcesso', 'id_cadeira',
                    existing_type=sa.String(length=20),
                    type_=sa.String(length=10),
                    existing_nullable=False)

    op.alter_column('SolicitacaoAcessoEspecial', 'id_turma',
                    existing_type=sa.String(length=20),
                    type_=sa.String(length=10),
                    existing_nullable=False)
    op.alter_column('SolicitacaoAcessoEspecial', 'id_cadeira',
                    existing_type=sa.String(length=20),
                    type_=sa.String(length=10),
                    existing_nullable=False)
