from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.core.database import Base

class Professor(Base):
    __tablename__ = "Professor"
    
    id = Column(Integer, ForeignKey('Usuario.id'), primary_key=True)
    departamento = Column(String(100), nullable=False)
    
    usuario = relationship("Usuario", back_populates="professor")
    turmas = relationship("Turma", back_populates="professor")
    