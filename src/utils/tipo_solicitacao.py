from enum import Enum


class SituacaoSolicitacao(Enum):
    PENDDENTE = "PENDENTE"
    REJEITADO = "REJEITADO"
    ACEITE = "ACEITE"