from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import time

from src.schemas.turma import TurmaResponse, TurmaAlunoResponse
from src.db_models.Cadeira import Cadeira
from src.db_models.Professor import Professor
from src.db_models.Turma import Turma
from src.db_models.Aluno import Aluno
from src.db_models.TurmaAluno import TurmaAluno

def registrar_turma(turma: TurmaResponse, db: Session):
    cadeira = db.query(Cadeira).filter_by(codigo=turma.codigo_cadeira).first()
    prof = db.query(Professor).filter_by(id=turma.professor_id).first()
    
    if not cadeira:
        cadeira = Cadeira(
            nome=turma.nome_cadeira,
            codigo=turma.codigo_cadeira
        )
        db.add(cadeira)
        db.commit()
    if not prof:
        raise HTTPException(status_code=400, detail="Professor inexistente.")
    
    nova_turma = Turma(
        codigo_turma=turma.codigo_turma,
        sala=turma.sala,
        dia_semana=turma.dia_semana,
        hora_inicio=turma.hora_inicio,
        hora_fim=turma.hora_fim,
        cadeira_id=cadeira.id,
        professor_id=prof.id
    )
    
    db.add(nova_turma)
    db.commit()
    db.refresh(nova_turma)
    
    return TurmaResponse(
        codigo_turma=nova_turma.codigo_turma,
        sala=nova_turma.sala,
        dia_semana=nova_turma.dia_semana,
        hora_inicio=nova_turma.hora_inicio,
        hora_fim=nova_turma.hora_fim,
        nome_cadeira=cadeira.nome,
        codigo_cadeira=cadeira.codigo,
        professor_id=prof.id
    )

def add_aluno(codigo_turma: str, aluno_id: int, db: Session):
    aluno = db.query(Aluno).filter_by(id=aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=400, detail="Auno inexistente.")

    turma = db.query(Turma).filter_by(codigo_turma=codigo_turma).first()
    if not turma:
        raise HTTPException(status_code=400, detail="Turma inexistente.")
    
    turma_aluno = TurmaAluno(
        turma_id=turma.id,
        aluno_id=aluno.id
    )
    
    db.add(turma_aluno)
    db.commit()
    db.refresh(turma_aluno)
    
    return TurmaAlunoResponse(
        aluno=aluno.usuario.nome,
        turma=turma.codigo_turma
    )
    