from sqlalchemy import Column, Integer, Identity, String
from sqlalchemy.orm import relationship
from src.core.database import Base

class TableUsuario(Base):
    __tablename__ = "Usuario"
    
    id = Column(Integer, primary_key=True)
    face_encodings = Column(String, nullable=False)
    
    acessos = relationship("TableControleAcesso", back_populates="usuario")
    solicitacoes = relationship("TableSolicitacaoAcessoEspecial", back_populates="usuario")