from datetime import datetime
from enum import Enum
from src.services.controle_acesso_service import registrar_acesso
from sqlalchemy.orm import Session


class StatusEntrada(Enum):
    PONTUAL = "pontual"
    PARCIAL = "parcial"
    FORA_DO_TEMPO = "fora_do_tempo"


class ControleAcesso():
    def __init__(self, data_hora_entrada: datetime, status_entrada: StatusEntrada, acesso_especial: bool, id_usuario: int, id_turma: int):
        self.data_hora_entrada = data_hora_entrada
        self.status_entrada = status_entrada
        self.acesso_especial = acesso_especial
        self.id_usuario = id_usuario
        self.id_turma = id_turma
        
    def registrar_entrada(self, db: Session):
        registrar_acesso(
            data_hora_entrada=self.data_hora_entrada,
            status_entrada=self.status_entrada,
            acesso_especial=self.acesso_especial,
            usuario=self.id_usuario,
            turma=self.id_turma,
            db=db
        )
    
    def verificar_status(self):
        return f"{self.status_entrada}"
