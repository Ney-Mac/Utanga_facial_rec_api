from sqlalchemy import Column, Integer, ForeignKey, ForeignKeyConstraint, Float, Boolean
from sqlalchemy.orm import relationship
from src.core.database import Base


class Dispensa(Base):
    __tablename__ = "Dispensa"

    id_dispensa = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nota_p1 = Column(Float, nullable=False)
    nota_p2 = Column(Float, nullable=False)
    dispensado = Column(Boolean, nullable=False)
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
        back_populates="dispensas",
        passive_deletes=True,
    )
    turma_cadeira = relationship(
        "Turma_Cadeira",
        back_populates="dispensas",
        passive_deletes=True,
    )
