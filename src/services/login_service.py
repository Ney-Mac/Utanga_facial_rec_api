import json
import numpy as np
import face_recognition as fr

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.db_models.Usuario import Usuario
from src.db_models.Administrador import Administrador
from src.db_models.Aluno import Aluno
from src.db_models.Professor import Professor

from src.utils.proccess_image import proccess_image
from src.schemas.auth import UserResponse
from src.utils.TipoUsuario import TipoUsuario


def fazer_login(image, db: Session):
    img_encodings = proccess_image(image)
    
    if not img_encodings:
        raise HTTPException(status_code=400, detail="Nenhum rosto detectado.")
    if len(img_encodings) > 1:
        raise HTTPException(status_code=400, detail="A imagem não pode conter mais de uma pessoa.")

    users = db.query(Usuario).all()
    
    for user in users:
        try:
            user_encodings = np.array(json.loads(user.foto_hash))
        except Exception:
            continue
        
        match = fr.compare_faces([user_encodings], img_encodings[0], tolerance=0.45)
        
        if match[0]:
            user_data = UserResponse(
                id=user.id,
                nome=user.nome,
                tipo=user.tipo,
                codigo_acesso=user.codigo_acesso
            )
            
            if user.tipo == TipoUsuario.ALUNO:
                aluno = db.query(Aluno).filter_by(id=user.id).first()
                if aluno:
                    user_data.curso = aluno.curso
                    
            elif user.tipo == TipoUsuario.PROFESSOR:
                prof = db.query(Professor).filter_by(id=user.id).first()
                if prof:
                    user_data.departamento = prof.departamento
                    
            else:
                adm = db.query(Administrador).filter_by(id=user.id).first()
                if adm:
                    user_data.nivel = adm.nivel
            
            return user_data
        
    raise HTTPException(status_code=401, detail="Usuário não reconhecido.")
    