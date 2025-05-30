from sqlalchemy import Column, Integer, Identity, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.core.database import Base
from src.utils.tipo_solicitacao import SituacaoSolicitacao


class TableSolicitacaoAcessoEspecial(Base):
    __tablename__= "SolicitacaoAcessoEspecial"
    
    id = Column(Integer, Identity(1,1), primary_key=True)
    situacao = Column(Enum(SituacaoSolicitacao, name="situacao"), nullable=False)
    data_hora_pedido = Column(DateTime, nullable=False)
    data_hora_resposta = Column(DateTime, nullable=True)
    id_turma = Column(String(20), nullable=False)
    id_cadeira = Column(String(20), nullable=False)
    id_usuario = Column(Integer, ForeignKey("Usuario.id"), nullable=False)
    
    usuario = relationship("TableUsuario", back_populates="solicitacoes")