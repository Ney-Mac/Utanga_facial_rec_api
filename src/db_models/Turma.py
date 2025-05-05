from sqlalchemy import Column, Integer, String, Enum, Time, ForeignKey
from sqlalchemy.orm import relationship
from src.core.database import Base
from src.utils.DiaSemana import DiaSemana


class Turma(Base):
    __tablename__ = "Turma"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_turma = Column(String(20), nullable=False, unique=True)
    sala = Column(String(50))
    dia_semana = Column(Enum(DiaSemana), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    
    cadeira_id = Column(Integer, ForeignKey("Cadeira.id"), nullable=False)
    professor_id = Column(Integer, ForeignKey("Professor.id"), nullable=False)
    
    cadeira = relationship("Cadeira", back_populates="turmas")
    professor = relationship("Professor", back_populates="turmas")
    alunos = relationship("TurmaAluno", back_populates="turma")
    