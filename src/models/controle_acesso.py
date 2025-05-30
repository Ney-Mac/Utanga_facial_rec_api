from sqlalchemy import Column, Integer, Identity, Date, Time, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.core.database import Base
from src.utils.tipo_acesso import TipoAcesso

class TableControleAcesso(Base):
    __tablename__ = "ControleAcesso"
    
    id = Column(Integer, Identity(1,1), primary_key=True)
    data_criacao = Column(Date, nullable=False)
    hora_criacao = Column(Time, nullable=False)
    tipo = Column(Enum(TipoAcesso, name="tipo"), nullable=False)
    id_turma = Column(String(20), nullable=False)
    id_cadeira = Column(String(20), nullable=False)
    id_usuario = Column(Integer, ForeignKey("Usuario.id"))
    
    usuario = relationship("TableUsuario", back_populates="acessos")    
