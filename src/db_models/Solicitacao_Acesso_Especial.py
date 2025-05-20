from sqlalchemy import Column, Integer, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from src.core.database import Base


class Solicitacao_Acesso_Especial(Base):
    __tablename__ = "Solicitacao_Acesso_Especial"

    id_solicitacao = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status_solicitacao = Column(
        Enum('pendente', 'aceite', 'rejeitado', name="status_solicitacao"),
        nullable=False,
    )
    data_resposta = Column(Date, nullable=False)
    id_usuario_solicitante = Column(
        Integer,
        ForeignKey("Usuario.id_usuario", ondelete="CASCADE"),
        nullable=False,
    )
    id_turma_destino = Column(
        Integer,
        ForeignKey("Turma.id_turma", ondelete="SET NULL"),
        nullable=True,
    )

    usuario = relationship(
        "Usuario",
        back_populates="solicitacoes",
        passive_deletes=True,
    )
    turma = relationship(
        "Turma",
        back_populates="solicitacoes",
        passive_deletes=True,
    )
