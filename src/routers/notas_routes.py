from fastapi import APIRouter, Depends, responses, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.services.notas_service import registrar_nota


router = APIRouter(prefix='/lancar-notas')


@router.post('/')
def lancar_notas(id_adm: int, nota_p1: float, nota_p2: float, id_aluno: int, id_turma: int, id_cadeira: int, db: Session = Depends(get_db)):
    try:
        dispensa = registrar_nota(
            id_adm=id_adm,
            nota_p1=nota_p1,
            nota_p2=nota_p2,
            id_aluno=id_aluno,
            id_cadeira=id_cadeira,
            id_turma=id_turma,
            db=db
        )
        
        return {
            "message": "Notas registradas!",
            "dispensa": dispensa
        }
        
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
        
