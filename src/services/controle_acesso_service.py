from sqlalchemy.orm import Session
from datetime import datetime
from src.db_models.Controle_Acesso import Controle_Acesso


def registrar_acesso(data_hora_entrada: datetime, status_entrada: str, acesso_especial: bool, usuario: int, turma: int, db: Session):
    novo_acesso = Controle_Acesso(
        data_hora_entrada=data_hora_entrada,
        status_entrada=status_entrada,
        acesso_especial=acesso_especial,
        id_usuario=usuario,
        id_turma=turma
    )
    
    db.add(novo_acesso)
    db.commit()
    db.refresh(novo_acesso)
