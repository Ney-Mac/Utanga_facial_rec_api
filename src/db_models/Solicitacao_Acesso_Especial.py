from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from src.core.database import Base

class SolicitacaoAcessoEspecial(Base):
    __tablename__ = "SolicitacaoAcessoEspecial"

    id = Column(Integer, primary_key=True, autoincrement=True)
    situacao = Column(String(9), nullable=False)
    data_hora_pedido = Column(DateTime, nullable=False)
    data_hora_resposta = Column(DateTime, nullable=True)
    id_turma = Column(String(20), nullable=False)
    id_cadeira = Column(String(20), nullable=False)
    estudante = Column(String(20), ForeignKey("Usuario.id", ondelete="SET NULL"))
    professor = Column(String(20), ForeignKey("Usuario.id", ondelete="SET NULL"))

    __table_args__ = (
        CheckConstraint("situacao IN ('PENDENTE', 'ACEITE', 'REJEIADO')", name="chk_situacao_acesso"),
    )
