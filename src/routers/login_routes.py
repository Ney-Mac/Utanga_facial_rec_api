from fastapi import APIRouter, responses, HTTPException, File, UploadFile, Depends
from src.utils.load_image import load_image
from src.services import login_service
from schemas.auth import AuthResponse
from src.core.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/login")


@router.post("/", response_model=AuthResponse)
async def fazer_login(image: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        img_content = await load_image(image)
        user = login_service.fazer_login(img_content, db=db)
        
        return { 
            "message": "Logado com sucesso.",
            "user": user
        }
    except HTTPException as http_error:
        print(f'Erro ao fazer login: {http_error}')
        return  responses.JSONResponse(
            status_code=http_error.status_code,
            content={ "message": http_error.detail }
        )
    except Exception as e:
        print(f'Erro ao fazer login: {e}')
        return responses.JSONResponse(
            status_code=500, 
            content={ "message": "Falha do servidor." }
        )
    
