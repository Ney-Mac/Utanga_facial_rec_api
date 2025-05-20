from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.database import Base


class Turma(Base):
    __tablename__ = "Turma"

    id_turma = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_turma = Column(String(20), nullable=False, unique=True)

    usuarios = relationship("Usuario", back_populates="turma", passive_deletes=True)
    cadeiras = relationship("Turma_Cadeira", back_populates="turma", cascade="all, delete-orphan", passive_deletes=True)
    acessos = relationship("Controle_Acesso", back_populates="turma", cascade="all, delete-orphan", passive_deletes=True)
    solicitacoes = relationship("Solicitacao_Acesso_Especial", back_populates="turma", cascade="all, delete-orphan", passive_deletes=True)
    # faltas = relationship("Falta", back_populates="turma_cadeira", cascade="all, delete-orphan", passive_deletes=True)
    # horarios = relationship("Horario", back_populates="turma", cascade="all, delete-orphan", passive_deletes=True)
