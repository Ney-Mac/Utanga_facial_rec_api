from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.core.database import Base

class Aluno(Base):
    __tablename__ = "Aluno"
    
    id = Column(Integer, ForeignKey('Usuario.id'), primary_key=True)
    curso = Column(String(100), nullable=False)
    
    usuario = relationship("Usuario", back_populates="aluno")
    turmas = relationship("TurmaAluno", back_populates="aluno")
    