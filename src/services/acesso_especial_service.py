from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date

from src.db_models.usuario import Usuario
from src.db_models.solicitacao_acesso_especial import SolicitacaoAcessoEspecial


def responder_pedido(id_acesso: int, aceitar: bool, db: Session):
    pedido_acesso = db.query(SolicitacaoAcessoEspecial).filter_by(id_solicitacao=id_acesso).first()
    if not pedido_acesso:
        raise HTTPException(status_code=400, detail="Nenhum pedido com esse id.")
    
    pedido_acesso.data_hora_resposta = date.today()
    pedido_acesso.situacao = "ACEITE" if aceitar else "REJEITADO"
    
    db.commit()
    db.refresh(pedido_acesso)
    
    return f"Pedido {'aceito' if aceitar else 'rejeitado'} com sucesso."

def solicitar_acesso(id_usuario: int, id_turma: int, db: Session):
    user = db.query(Usuario).filter_by(id_usuario=id_usuario, id_turma=id_turma).first()
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não identificado ou não pertencente a turma.")

    nova_solicitacao = SolicitacaoAcessoEspecial(
        status_solicitacao="pendente",
        data_resposta=date.today(),
        id_usuario_solicitante=id_usuario,
        id_turma_destino=id_turma
    )
    
    db.add(nova_solicitacao)
    db.commit()
    db.refresh(nova_solicitacao)
    
    return {
        "message": "Solicitação pendente, aguarde a resposta do Professor.",
        "solicitacao": {
            "id_solicitacao": nova_solicitacao.id,
            "status_solicitacao": nova_solicitacao.situacao,
            "solicitante": nova_solicitacao.estudante 
        }
    }
