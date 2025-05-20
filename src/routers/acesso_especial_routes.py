from fastapi import APIRouter, Depends, responses, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.services.acesso_especial_service import responder_pedido

from src.models.Usuario import Usuario
from src.db_models.Usuario import Usuario as DB_User

from src.models.SolicitacaoAcessoEspecial import SolicitacaoAcessoEspecial
from src.db_models.Solicitacao_Acesso_Especial import Solicitacao_Acesso_Especial


router = APIRouter(prefix='/acesso-especial')


@router.post('/responder')
def responder_pedido_acesso_especial(id_solicitacao: int, aceitar: bool, db: Session = Depends(get_db)):
    try:
        pedido_acesso = db.query(Solicitacao_Acesso_Especial).filter_by(id_solicitacao=id_solicitacao).first()
        if not pedido_acesso:
            raise HTTPException(status_code=400, detail="Nenhum pedido com esse id.")

        solicitacao = SolicitacaoAcessoEspecial(
            id=pedido_acesso.id_solicitacao,
            status_solicitacao=pedido_acesso.status_solicitacao,
            data_resposta=pedido_acesso.data_resposta,
            id_usuario=pedido_acesso.id_usuario_solicitante,
            id_turma=pedido_acesso.id_turma_destino
        )
        
        if aceitar:
            return solicitacao.aceitar_acesso(db)
        else:
            return solicitacao.negar_acesso(db)
        
    except HTTPException as http_error:
        print(f'Erro ao responder pedidio de acesso especial: {http_error}')
        return  responses.JSONResponse(
            status_code=http_error.status_code,
            content={ "message": http_error.detail }
        )
    except Exception as e:
        print(f'Erro ao responder pedidio de acesso especial: {e}')
        return responses.JSONResponse(
            status_code=500, 
            content={ "message": "Falha do servidor." }
        )

@router.post('/solicitar')
def solicitar_acesso_especial(id_usuario: int, id_turma_destino: int, db: Session = Depends(get_db)):
    try:
        user = db.query(DB_User).filter_by(id_usuario=id_usuario, id_turma=id_turma_destino).first()
        if not user:
            raise HTTPException(status_code=400, detail="Usuário não identificado ou não pertencente a turma.")

        usuario = Usuario(
            id=user.id_usuario,
            nome=f"Usuario {id_usuario}",
            matricula=user.id_usuario,
            dados_face=user.foto_hash,
            ano_lectivo="2025",
            curso="Informatica",
            id_turma=user.id_turma,
            tipo=user.tipo
        )
        
        return usuario.solicitar_acesso_especial(db)
    
    except HTTPException as http_error:
        print(f'Erro ao solicitar acesso especial: {http_error}')
        return  responses.JSONResponse(
            status_code=http_error.status_code,
            content={ "message": http_error.detail }
        )
    except Exception as e:
        print(f'Erro ao solicitar acesso especial: {e}')
        return responses.JSONResponse(
            status_code=500, 
            content={ "message": "Falha do servidor." }
        )
        