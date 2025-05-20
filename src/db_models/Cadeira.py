from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.database import Base


class Cadeira(Base):
    __tablename__ = "Cadeira"

    id_cadeira = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_cadeira = Column(String(20), nullable=False, unique=True)

    turmas = relationship("Turma_Cadeira", back_populates="cadeira", cascade="all, delete-orphan", passive_deletes=True)
    # horarios = relationship("Horario", back_populates="cadeira", passive_deletes=True)
