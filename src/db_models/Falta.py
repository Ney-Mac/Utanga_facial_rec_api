from sqlalchemy import Column, Integer, ForeignKey, Enum, Date, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from src.core.database import Base


class Falta(Base):
    __tablename__ = "Falta"

    id_falta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo_falta = Column(Enum('total', 'parcial', name="tipo_falta"), nullable=False)
    data_falta = Column(Date, nullable=False)
    id_usuario = Column(Integer, ForeignKey("Usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    id_turma = Column(Integer, nullable=False)
    id_cadeira = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['id_turma', 'id_cadeira'],
            ['Turma_Cadeira.id_turma', 'Turma_Cadeira.id_cadeira'],
            ondelete="CASCADE"
        ),
    )

    usuario = relationship("Usuario", back_populates="faltas", passive_deletes=True)
    turma_cadeira = relationship("Turma_Cadeira", back_populates="faltas", passive_deletes=True)
