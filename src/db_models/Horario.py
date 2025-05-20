from sqlalchemy import Column, Integer, ForeignKey, Enum, Time, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from src.core.database import Base


class Horario(Base):
    __tablename__ = "Horario"

    id_horario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_turma = Column(Integer, nullable=False)
    id_cadeira = Column(Integer, nullable=False)
    dia = Column(Enum('seg', 'ter', 'qua', 'qui', 'sex', name="dia_semana"), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['id_turma', 'id_cadeira'],
            ['Turma_Cadeira.id_turma', 'Turma_Cadeira.id_cadeira'],
            ondelete="CASCADE"
        ),
    )
    
    turma_cadeira = relationship("Turma_Cadeira", back_populates="horarios", passive_deletes=True)

    # turma = relationship("Turma", back_populates="horarios", passive_deletes=True)
    # cadeira = relationship("Cadeira", back_populates="horarios", passive_deletes=True)
