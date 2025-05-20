from sqlalchemy import Column, Integer, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from src.core.database import Base


class Controle_Acesso(Base):
    __tablename__ = "Controle_Acesso"

    id_acesso = Column(Integer, primary_key=True,
                       index=True, autoincrement=True)
    data_hora_entrada = Column(DateTime, nullable=False)
    status_entrada = Column(
        Enum("pontual", "parcial", "fora_do_limite", name="status_entrada"),
        nullable=False,
    )
    acesso_especial = Column(Boolean, nullable=False)
    id_usuario = Column(
        Integer,
        ForeignKey("Usuario.id_usuario", ondelete="CASCADE"),
        nullable=False,
    )
    id_turma_acessada = Column(
        Integer,
        ForeignKey("Turma.id_turma", ondelete="SET NULL"),
        nullable=True,
    )

    usuario = relationship(
        "Usuario",
        back_populates="acessos",
        passive_deletes=True,
    )
    turma = relationship(
        "Turma",
        back_populates="acessos",
        passive_deletes=True,
    )
