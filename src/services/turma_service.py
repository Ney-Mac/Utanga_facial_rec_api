# from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from src.db_models.Turma import Turma


def listar_turmas(id: Optional[str], nome: Optional[str], db: Session):
    filtros = []
    
    if id:
        filtros.append(Turma.id_turma == id)
    
    if nome:
        filtros.append(Turma.nome_turma == nome)
    
    turmas = db.query(Turma).filter(*filtros).all()
    
    if turmas:
        return turmas
    else:
        return []
