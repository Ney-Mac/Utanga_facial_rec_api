from enum import Enum
from datetime import date

from sqlalchemy.orm import Session
from src.services.acesso_especial_service import responder_pedido


class StatusSolicitacao(Enum):
    PENDENTE = "pendente"
    ACEITE = "aceite"
    REJEITADO = "rejeitado"


class SolicitacaoAcessoEspecial():
    def __init__(self, id: int, data_resposta: date, status_solicitacao: StatusSolicitacao, id_usuario: int, id_turma: int):
        self.id = id
        self.data_resposta = data_resposta
        self.status_solicitacao = status_solicitacao
        self.id_usuario = id_usuario
        self.id_turma = id_turma

    def aceitar_acesso(self, db: Session):
        return responder_pedido(
            id_acesso=self.id,
            aceitar=True,
            db=db
        )

    def negar_acesso(self, db: Session):
        return responder_pedido(
            id_acesso=self.id,
            aceitar=False,
            db=db
        )
