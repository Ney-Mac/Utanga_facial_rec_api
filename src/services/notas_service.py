from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.db_models.Usuario import Usuario
from src.db_models.Dispensa import Dispensa
from src.db_models.Turma_Cadeira import Turma_Cadeira


def registrar_nota(
        id_adm: int,
        nota_p1: float,
        nota_p2: float,
        id_aluno: int,
        db: Session,
        id_turma: int,
        id_cadeira: int
    ):
    
    adm = db.query(Usuario).filter_by(id_usuario=id_adm).first()
    if not adm or adm.tipo != 'adm':
        raise HTTPException(status_code=401, detail="Não autorizado!")

    aluno = db.query(Usuario).filter_by(id_usuario=id_aluno).first()
    if not aluno or aluno.tipo != 'aluno':
        raise HTTPException(status_code=400, detail="Aluno inexistente!")

    turma_cadeira = db.query(Turma_Cadeira).filter_by(id_turma=id_turma, id_cadeira=id_cadeira).first()
    if not turma_cadeira:
        raise HTTPException(status_code=400, detail=f"A Turma {id_turma} não existe ou não contém a Cadeira {id_cadeira}")

    media = (nota_p1 + nota_p2)/2 

    nova_dispensa = Dispensa(
        nota_p1=nota_p1,
        nota_p2=nota_p2,
        dispensado=media >= 14,
        id_usuario=id_aluno,
        id_turma=id_turma,
        id_cadeira=id_cadeira
    )
    
    db.add(nova_dispensa)
    db.commit()
    db.refresh(nova_dispensa)
    
    return nova_dispensa
    