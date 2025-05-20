from fastapi import APIRouter, HTTPException, responses, Depends
from fastapi import UploadFile, Form, File
from sqlalchemy.orm import Session

from typing import Optional

from src.services.users_services import listar_usuarios, registrar_usuario
from src.services.login_service import fazer_login

from src.utils.load_image import carregar_e_validar_imagem
from src.utils.validacao_de_campos import validar_campos_por_tipo

from src.core.database import get_db
from src.core.dependencies import validar_token


router = APIRouter(prefix="/usuario")


@router.post("/logar")
async def logar_usuario_endpoint(image: UploadFile = File(...), id_turma_destino: Optional[int] = Form(None), db: Session = Depends(get_db)):
    try:
        img = await carregar_e_validar_imagem(image)
        
        user = fazer_login(
            image=img,
            id_turma_destino=id_turma_destino,
            db=db
        )       
        
        return {
            "message": "Login realizado com sucesso.",
            "user": user
        } 
    
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


@router.post("/registrar")
async def registrar_usuarios_endpoint(
        image: UploadFile = File(...),
        nome: str = Form(...),
        tipo: str = Form(...),
        matricula: Optional[str] = Form(None),
        ano_letivo: Optional[str] = Form(None),
        curso: Optional[str] = Form(None),
        id_turma: Optional[int] = Form(None),
        db: Session = Depends(get_db),
        # _: dict = Depends(validar_token)
    ):
    """
    Adicionar dados dos usuários
    """
    try:
        validar_campos_por_tipo(
            ano_lectivo=ano_letivo,
            matricula=matricula,
            id_turma=id_turma,
            curso=curso,
            tipo=tipo
        )
        
        img = await carregar_e_validar_imagem(image)
        
        user = registrar_usuario(
            image=img,
            db=db,
            tipo=tipo,
            id_turma=id_turma,
            nome=nome,
            matricula=matricula,
            ano_letivo=ano_letivo,
            curso=curso
        )
        
        return {
            "message": "Usuário registrado com sucesso!",
            user: user
        }
        
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
async def listar_usuarios_endpoint(tipo: Optional[str] = None, id_usuario: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Lista usuários, com filtro opcional por tipo ou ID.
    """

    try:
        if tipo and tipo not in ['aluno', 'prof', 'adm']:
            raise HTTPException(status_code=400, detail="Tipo incorrecto.")

        return listar_usuarios(
            tipo=tipo,
            id_usuario=id_usuario,
            db=db
        )

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
