from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from src.core.database import Base
from src.utils.TipoUsuario import TipoUsuario

class Usuario(Base):
    __tablename__ = 'Usuario'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(Enum(TipoUsuario), nullable=False)
    codigo_acesso = Column(String(50), nullable=False)
    foto_hash = Column(String(255))
    
    aluno = relationship("Aluno", uselist=False, back_populates="usuario")
    professor = relationship("Professor", uselist=False, back_populates="usuario")
    administrador = relationship("Administrador", uselist=False, back_populates="usuario")