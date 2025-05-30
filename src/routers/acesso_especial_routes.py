from fastapi import APIRouter, Depends, responses, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.services.acesso_especial_service import (
    responder_pedido,
    solicitar_acesso,
    listar_solicitacoes_acesso_filtrado,
    consultar_estado_solicitacao
)
from typing import Optional


router = APIRouter(prefix='/acesso-especial', tags=["Solicitação de Acesso Especial"])


@router.get('/consultar')
async def consultar_estado_pedido(id_usuario: str, id_turma_destino: str, db: Session = Depends(get_db)):
    try:
        res = await consultar_estado_solicitacao(id_usuario, id_turma_destino, db)
        return res
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
@router.post('/solicitar')
async def solicitar_acesso_especial_endpoint(id_usuario: str, id_turma_destino: str, db: Session = Depends(get_db)):
    try:
        res = await solicitar_acesso(
            id_usuario=id_usuario,
            id_turma_destino=id_turma_destino,
            db=db
        )
        return res
    
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

@router.post('/responder')
async def responder_pedido_acesso_especial_endpoint(id_solicitacao: int, aceitar: bool, db: Session = Depends(get_db)):
    try:
        res = await responder_pedido(
            id_solicitacao=id_solicitacao,
            aceitar=aceitar,
            db=db
        )
        return res
        
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

@router.get('/listar')
async def listar_solicitacoes_filtradas_endpoint(
    id_turma: Optional[str] = None,
    id_cadeira: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        res = await listar_solicitacoes_acesso_filtrado(
            db=db,
            id_turma=id_turma,
            id_cadeira=id_cadeira
        )
        return res

    except Exception as e:
        print(f'Erro ao listar solicitações filtradas: {e}')
        return responses.JSONResponse(
            status_code=500,
            content={ "message": "Falha do servidor." }
        )
