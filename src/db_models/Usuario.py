from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from src.core.database import Base


class Usuario(Base):
    __tablename__ = "Usuario"

    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    matricula = Column(String, nullable=True)
    ano_lectivo = Column(String, nullable=True)
    curso = Column(String, nullable=True)
    foto_hash = Column(String, nullable=True)
    tipo = Column(Enum('aluno', 'prof', 'adm', name="tipo_usuario"), nullable=False)
    id_turma = Column(Integer, ForeignKey("Turma.id_turma", ondelete="SET NULL"), nullable=True)

    turma = relationship("Turma", back_populates="usuarios", passive_deletes=True)
    acessos = relationship("Controle_Acesso", back_populates="usuario", cascade="all, delete-orphan", passive_deletes=True)
    faltas = relationship("Falta", back_populates="usuario", cascade="all, delete-orphan", passive_deletes=True)
    dispensas = relationship("Dispensa", back_populates="usuario", cascade="all, delete-orphan", passive_deletes=True)
    solicitacoes = relationship("Solicitacao_Acesso_Especial", back_populates="usuario", cascade="all, delete-orphan", passive_deletes=True)
    notas = relationship("Nota", back_populates="usuario", cascade="all, delete-orphan", passive_deletes=True)
