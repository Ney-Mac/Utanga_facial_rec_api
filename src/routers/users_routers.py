from fastapi import APIRouter, HTTPException, responses, Depends
from fastapi import UploadFile, Form, File
from sqlalchemy.orm import Session
from typing import Optional

from src.services.users_services import listar_usuarios, registrar_usuario, fazer_login
from src.utils.load_image import carregar_e_validar_imagem
from src.core.database import get_db


router = APIRouter(prefix="/usuario", tags=["Usuário"])


@router.post("/logar")
async def logar_usuario_endpoint(image: UploadFile = File(...), id_turma_destino: Optional[str] = Form(None), db: Session = Depends(get_db)):
    try:
        img = await carregar_e_validar_imagem(image)
        
        user = await fazer_login(
            image=img,
            id_turma_destino=id_turma_destino,
            db=db
        )
        
        return user
    
    except HTTPException as http_error:
        print(f'Erro ao logar usuário: {http_error}')
        return responses.JSONResponse(
            status_code=http_error.status_code,
            content={"message": http_error.detail}
        )
    except Exception as e:
        print(f'Erro ao logar usuário: {e}')
        return responses.JSONResponse(
            status_code=500,
            content={"message": "Falha do servidor."}
        )


@router.post("/registrar")
async def registrar_usuarios_endpoint(
        image: UploadFile = File(...),
        id_usuario: str = File(...),
        db: Session = Depends(get_db),
    ):
    """
    Adicionar dados dos usuários
    """
    try:
        img = await carregar_e_validar_imagem(image)
        res = await registrar_usuario(image=img, id_usuario=id_usuario, db=db)
        return res
        
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


@router.get("/")
async def listar_usuarios_endpoint(tipo: Optional[str] = None, id_usuario: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Lista usuários, com filtro opcional por tipo ou ID.
    """
    
    try:
        if tipo and tipo not in ['estudante', 'prof', 'adm']:
            raise HTTPException(status_code=400, detail="Tipo incorrecto. Tente um destes: estudante, adm, prof")

        res = await listar_usuarios(
            tipo=tipo,
            id_usuario=id_usuario,
            db=db
        )
        
        return res

    except HTTPException as http_error:
        print(f'Erro ao listar usuários: {http_error}')
        return responses.JSONResponse(
            status_code=http_error.status_code,
            content={"message": http_error.detail}
        )
    except Exception as e:
        print(f'Erro ao listar usuários: {e}')
        return responses.JSONResponse(
            status_code=500,
            content={"message": "Falha do servidor."}
        )

