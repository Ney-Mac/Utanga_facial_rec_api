from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.database import Base


class Cadeira(Base):
    __tablename__ = "Cadeira"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    codigo = Column(String(20), nullable=False)
    
    turmas = relationship("Turma", back_populates="cadeira")
