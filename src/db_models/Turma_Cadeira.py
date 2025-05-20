from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.core.database import Base


class Turma_Cadeira(Base):
    __tablename__ = "Turma_Cadeira"

    id_turma = Column(Integer, ForeignKey("Turma.id_turma", ondelete="CASCADE"), primary_key=True)
    id_cadeira = Column(Integer, ForeignKey("Cadeira.id_cadeira", ondelete="CASCADE"), primary_key=True)

    turma = relationship("Turma", back_populates="cadeiras", passive_deletes=True)
    cadeira = relationship("Cadeira", back_populates="turmas", passive_deletes=True)
    notas = relationship("Nota", back_populates="turma_cadeira", cascade="all, delete-orphan", passive_deletes=True)
    dispensas = relationship("Dispensa", back_populates="turma_cadeira", cascade="all, delete-orphan", passive_deletes=True)
    horarios = relationship("Horario", back_populates="turma_cadeira", passive_deletes=True)
    faltas = relationship("Falta", back_populates="turma_cadeira", passive_deletes=True)
