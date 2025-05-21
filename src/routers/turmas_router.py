from fastapi import APIRouter, HTTPException, responses, Depends
from sqlalchemy.orm import Session
from src.db_models.Turma import Turma
from typing import Optional
from src.core.database import get_db
from src.services.turma_service import listar_turmas


router = APIRouter(prefix="/turma")


@router.get("/")
async def listar_turmas_endpoint(id: Optional[str] = None, nome: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Lista turmas, com filtro opcional por ID ou Nome.
    """
    
    try:
        return listar_turmas(id=id, nome=nome, db=db)
    except HTTPException as http_error:
        print(f'Erro ao registrar usuário: {http_error}')
        return responses.JSONResponse(
            status_code=http_error.status_code,
            content={"message": http_error.detail}
        )
    except Exception as e:
        print(f'Erro ao registrar usuário: {e}')
        return responses.JSONResponse(
            status_code=500,
            content={"message": "Falha do servidor."}
        )
    