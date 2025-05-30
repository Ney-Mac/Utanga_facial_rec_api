from fastapi import HTTPException, responses, Depends, APIRouter
from src.services.controle_acesso_service import buscar_acesso, buscar_acessos_por_turma
from sqlalchemy.orm import Session
from src.core.database import get_db


router = APIRouter(prefix='/controle-acesso', tags=["Controle de acessos"])


@router.get('/')
async def listar_acessos(db: Session = Depends(get_db)):
    try:
        return await buscar_acesso(db)
    except HTTPException as http_error:
        print(f'Erro ao listar acessos: {http_error}')
        return  responses.JSONResponse(
            status_code=http_error.status_code,
            content={ "message": http_error.detail }
        )
    except Exception as e:
        print(f'Erro ao listar acessos especial: {e}')
        return responses.JSONResponse(
            status_code=500, 
            content={ "message": "Falha do servidor." }
        )
        
@router.get("/acessos-turma/{id_turma}")
async def acesso_por_turma(id_turma: str, db: Session = Depends(get_db)):
    try:
        return await buscar_acessos_por_turma(id_turma=id_turma, db=db)
    except HTTPException as http_error:
        print(f'Erro ao listar acessos: {http_error}')
        return  responses.JSONResponse(
            status_code=http_error.status_code,
            content={ "message": http_error.detail }
        )
    except Exception as e:
        print(f'Erro ao listar acessos especial: {e}')
        return responses.JSONResponse(
            status_code=500, 
            content={ "message": "Falha do servidor." }
        )
        

