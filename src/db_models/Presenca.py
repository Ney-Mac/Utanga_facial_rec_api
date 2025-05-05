from sqlalchemy import Column, Integer, Enum, ForeignKeyConstraint, Date
from sqlalchemy.orm import relationship
from src.utils.StatusPresenca import StatusPresenca
from src.core.database import Base


class Presenca(Base):
    __tablename__ = "Presenca"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    turma_id = Column(Integer, nullable=False)
    aluno_id = Column(Integer, nullable=False)
    data = Column(Date, nullable=False)
    status = Column(Enum(StatusPresenca), nullable=False)
    
    __table_args__ = (
        ForeignKeyConstraint(
            ['turma_id', 'aluno_id'],
            ['Turma_Aluno.turma_id', 'Turma_Aluno.aluno_id']
        ),
    )
    
    turma_aluno = relationship("TurmaAluno", back_populates="presencas")    
    