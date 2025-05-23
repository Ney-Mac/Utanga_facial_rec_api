from sqlalchemy import Column, Integer, Date, Time, String, ForeignKey, CheckConstraint
from src.core.database import Base

class ControleAcesso(Base):
    __tablename__ = "ControleAcesso"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_criacao = Column(Date, nullable=False)
    hora_criacao = Column(Time, nullable=False)
    tipo = Column(String(9), nullable=False)
    id_turma = Column(Integer, nullable=False)
    id_cadeira = Column(Integer, nullable=False)
    id_usuario = Column(String(20), ForeignKey("Usuario.id", ondelete="SET NULL"))

    __table_args__ = (
        CheckConstraint("tipo IN ('PERMITIDO', 'BLOQUEADO')", name="chk_tipo_acesso"),
    )
