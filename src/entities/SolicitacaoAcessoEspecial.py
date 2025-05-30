from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.solicitacao_acesso_especial import TableSolicitacaoAcessoEspecial
from src.utils.tipo_solicitacao import SituacaoSolicitacao

from .ControleAcesso import ControleAcesso
from src.utils.tipo_acesso import TipoAcesso

class SolicitacaoAcessoEspecial:
    def __init__(self, id: int, situacao: SituacaoSolicitacao, data_hora_pedido, data_hora_resposta, id_turma, id_cadeira, estudante):
        self.id = id
        self.situacao = situacao
        self.data_hora_pedido = data_hora_pedido
        self.data_hora_resposta = data_hora_resposta
        self.id_turma = id_turma
        self.id_cadeira = id_cadeira
        self.estudante = estudante
        
    def aceitar_acesso_especial(self, db: Session):
        try:
            solicitacao = db.query(TableSolicitacaoAcessoEspecial).filter_by(id=self.id).first()
            if not solicitacao:
                raise HTTPException(status_code=404, detail="Não há enhuma Solicitação de Acesso Especial com esse id.")
            
            agora = datetime.now()
            
            solicitacao.situacao = SituacaoSolicitacao.ACEITE
            solicitacao.data_hora_resposta = agora
            self.situacao = SituacaoSolicitacao.ACEITE
            self.data_hora_resposta = agora
            
            db.add(solicitacao)
            db.commit()
            db.refresh(solicitacao)
            
            novo_acesso = ControleAcesso(
                hora_criacao=agora.time(),
                data_criacao=agora.date(),
                tipo=TipoAcesso.ACEITE,
                id_turma=self.id_turma,
                id_cadeira=self.id_cadeira,
                id_usuario=self.estudante
            )
            novo_acesso.registrar_entrada(db)
            
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail="Falha ao aceitar solicitação de acesso especial.")
    
    def negar_acesso_especial(self, db: Session):
        try:
            solicitacao = db.query(TableSolicitacaoAcessoEspecial).filter_by(id=self.id).first()
            if not solicitacao:
                raise HTTPException(status_code=404, detail="Não há enhuma Solicitação de Acesso Especial com esse id.")
            
            solicitacao.situacao = SituacaoSolicitacao.REJEITADO
            solicitacao.data_hora_resposta = datetime.now()
            self.situacao = SituacaoSolicitacao.REJEITADO
            self.data_hora_resposta = datetime.now()
            
            db.add(solicitacao)
            db.commit()
            db.refresh(solicitacao)
            
            return False
        except Exception:
            raise HTTPException(status_code=500, detail="Falha ao aceitar solicitação de acesso especial.")
    