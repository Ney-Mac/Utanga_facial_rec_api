from fastapi import APIRouter, File, UploadFile, HTTPException, Form, responses, Depends
from sqlalchemy.orm import Session
from src.services import cadastro_service
from src.utils.load_image import load_image
from src.utils.NivelAdmin import NivelAdmin
from src.schemas.auth import AuthResponse
from src.core.database import get_db


router = APIRouter(prefix="/cadastrar")


@router.post("/aluno", response_model=AuthResponse)
async def cadastrar_aluno(
        nome: str = Form(...),
        numero_matricula: str = Form(...),
        curso: str = Form(...),
        image: UploadFile = File(...),
        db: Session = Depends(get_db)
    ):
    
    try:
        img_content = await load_image(image)
        
        user = cadastro_service.registrar_aluno(
            nome=nome,
            numero_matricula=numero_matricula,
            curso=curso,
            image=img_content,
            db=db
        )

        return {
            "message": "Aluno criado com sucesso.",
            "user": user
        }
    except HTTPException as http_error:
        print(f'Erro ao cadastrar aluno: {http_error}')
        return  responses.JSONResponse(
            status_code=http_error.status_code,
            content={ "message": http_error.detail }
        )
    except Exception as e:
        print(f'Erro ao cadastrar aluno: {e}')
        return responses.JSONResponse(
            status_code=500, 
            content={ "message": "Falha do servidor." }
        )

     
@router.post("/professor", response_model=AuthResponse)
async def cadastrar_professor(
        nome: str = Form(...),
        numero_funcionario: str = Form(...),
        departamento: str = Form(...),
        image: UploadFile = File(...),
        db: Session = Depends(get_db)
    ):
    
    try:
        img_content = await load_image(image)
        user = cadastro_service.registrar_professor(
            nome=nome,
            numero_funcionario=numero_funcionario,
            departamento=departamento,
            image=img_content,
            db=db
        )

        return {
            "message": "Professor criado com sucesso.",
            "user": user
        }
    except HTTPException as http_error:
        print(f'Erro ao cadastrar professor: {http_error}')
        return  responses.JSONResponse(
            status_code=http_error.status_code,
            content={ "message": http_error.detail }
        )
    except Exception as e:
        print(f'Erro ao cadastrar professor: {e}')
        return responses.JSONResponse(
            status_code=500, 
            content={ "message": "Falha do servidor." }
        )

        
@router.post("/administrador", response_model=AuthResponse)
async def cadastrar_administrador(
        nome: str = Form(...),
        numero_funcionario: str = Form(...),
        nivel: str = Form(...),
        image: UploadFile = File(...),
        db: Session = Depends(get_db)
    ):
    
    try:
        if nivel not in [e.value for e in NivelAdmin]:
            raise HTTPException(status_code=400, detail="Nivel inválido.")
        
        img_content = await load_image(image)
        user = cadastro_service.registrar_administrador(
            nome=nome,
            numero_funcionario=numero_funcionario,
            nivel=nivel,
            image=img_content,
            db=db
        )
        
        return {
            "message": "Administrador criado com sucesso.",
            "user": user
        }
    except HTTPException as http_error:
        print(f'Erro ao cadastrar administrador: {http_error}')
        return  responses.JSONResponse(
            status_code=http_error.status_code,
            content={ "message": http_error.detail }
        )
    except Exception as e:
        print(f'Erro ao cadastrar administrador: {e}')
        return responses.JSONResponse(
            status_code=500, 
            content={ "message": "Falha do servidor." }
        )
