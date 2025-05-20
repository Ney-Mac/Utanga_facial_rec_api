from sqlalchemy import Column, Integer, Float, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from src.core.database import Base


class Nota(Base):
    __tablename__ = "Nota"

    id_nota = Column(Integer, primary_key=True, autoincrement=True)
    nota_p1 = Column(Float)
    nota_p2 = Column(Float)

    id_usuario = Column(
        Integer,
        ForeignKey("Usuario.id_usuario", ondelete="CASCADE"),
        nullable=False,
    )
    id_turma = Column(Integer, nullable=False)
    id_cadeira = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["id_turma", "id_cadeira"],
            ["Turma_Cadeira.id_turma", "Turma_Cadeira.id_cadeira"],
            ondelete="CASCADE",
        ),
    )

    usuario = relationship(
        "Usuario",
        back_populates="notas",
        passive_deletes=True,
    )
    turma_cadeira = relationship(
        "Turma_Cadeira",
        back_populates="notas",
        passive_deletes=True,
    )
