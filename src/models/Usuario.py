from enum import Enum

from sqlalchemy.orm import Session
from src.services.acesso_especial_service import solicitar_acesso
from .Dispensa import Dispensa

class TipoUsuario(Enum):
    ALUNO = 'aluno'
    PROF = 'prof'
    ADM = 'adm'


class Usuario:
    def __init__(
        self,
        id: int,
        nome: str,
        matricula: str,
        dados_face: str,
        ano_lectivo: str,
        curso: str,
        id_turma: int,
        tipo: TipoUsuario
    ):

        self.id = id
        self.nome = nome
        self.matricula = matricula
        self.dados_face = dados_face
        self.ano_lectivo = ano_lectivo
        self.curso = curso
        self.id_turma = id_turma
        self.tipo = tipo

    def solicitar_acesso_especial(self, db: Session):
        return solicitar_acesso(
            id_usuario=self.id,
            id_turma=self.id_turma,
            db=db
        )

    def verificar_dispensa(self, dispensa: Dispensa):
        return dispensa.verificar_elegibilidade()
