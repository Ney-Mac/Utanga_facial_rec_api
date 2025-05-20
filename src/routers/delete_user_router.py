from fastapi import HTTPException, responses, APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db

from src.db_models.Usuario import Usuario


router = APIRouter(prefix='/apagar-usuario')


@router.delete('/')
async def apagar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    try: 
        usuario = db.query(Usuario).filter_by(id_usuario=id_usuario).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        
        db.delete(usuario)
        db.commit()
        
        return f"Usuario {id_usuario} eliminado"
        
    except HTTPException as http_error:
        print(f'Erro ao cadastrar usuário: {http_error}')
        return  responses.JSONResponse(
            status_code=http_error.status_code,
            content={ "message": http_error.detail }
        )
    except Exception as e:
        print(f'Erro ao cadastrar usuário: {e}')
        return responses.JSONResponse(
            status_code=500, 
            content={ "message": "Falha do servidor." }
        )