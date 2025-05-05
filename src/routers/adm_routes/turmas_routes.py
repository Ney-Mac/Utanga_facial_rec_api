from fastapi import APIRouter, HTTPException, responses, Depends, Query
from sqlalchemy.orm import Session
from datetime import time

from src.utils.DiaSemana import DiaSemana
from src.core.database import get_db
from src.services import turma_service
from src.schemas.turma import TurmaResponse, CreateTurmaResponse, TurmaAlunoResponse


router = APIRouter(prefix="/turma")


@router.post("/cadastro", response_model=CreateTurmaResponse)
async def cadastrar_turma(turma: TurmaResponse,db: Session = Depends(get_db)):
    
    try:
        turma = turma_service.registrar_turma(turma, db=db)
        
        return {
            "message": "Turma criada com sucesso.",
            "turma": turma
        }
    
    except HTTPException as http_error:
        print(f'Erro ao cadastrar turma: {http_error}')
        return  responses.JSONResponse(
            status_code=http_error.status_code,
            content={ "message": http_error.detail }
        )
    except Exception as e:
        print(f'Erro ao cadastrar turma: {e}')
        return responses.JSONResponse(
            status_code=500, 
            content={ "message": "Falha do servidor." }
        )

@router.post('/add-aluno')    
async def adicionar_aluno(codigo_turma: str = Query(...), aluno_id: int = Query(...), db: Session = Depends(get_db)):
    try:
        res: TurmaAlunoResponse = turma_service.add_aluno(codigo_turma, aluno_id, db)
        
        return {
            "message": f'Aluno {res.aluno} adicionado a turma {res.turma}.',
        }
    except HTTPException as http_error:
        print(f'Erro ao adicionar aluno a turma: {http_error}')
        return  responses.JSONResponse(
            status_code=http_error.status_code,
            content={ "message": http_error.detail }
        )
    except Exception as e:
        print(f'Erro ao adicionar aluno a turma: {e}')
        return responses.JSONResponse(
            status_code=500, 
            content={ "message": "Falha do servidor." }
        )
    