from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.utils.StatusAluno import StatusAluno
from src.core.database import Base


class TurmaAluno(Base):
    __tablename__ = "Turma_Aluno"
    
    turma_id = Column(Integer, ForeignKey("Turma.id"), primary_key=True, nullable=False)
    aluno_id = Column(Integer, ForeignKey("Aluno.id"), primary_key=True, nullable=False)
    status = Column(Enum(StatusAluno))
    
    turma = relationship("Turma", back_populates="alunos")
    aluno = relationship("Aluno", back_populates="turmas")
    
    presencas = relationship("Presenca", back_populates="turma_aluno")
    