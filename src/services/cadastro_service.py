import json
import numpy as np
import face_recognition as fr
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.db_models.Usuario import Usuario
from src.db_models.Aluno import Aluno
from src.db_models.Professor import Professor
from src.db_models.Administrador import Administrador

from src.utils.proccess_image import proccess_image

from src.schemas.auth import UserResponse
from src.utils.TipoUsuario import TipoUsuario


def registrar_aluno(nome: str, numero_matricula: str, curso: str, image, db: Session) -> UserResponse:
    img_encodings = proccess_image(image)
    
    validar_encodings(img_encodings)
    if validar_usuario_existe(db, img_encodings):
        raise HTTPException(status_code=400, detail="Usuário já registrado.")

    img_encodings = json.dumps(img_encodings[0].tolist())
    
    novo_usuario = Usuario(
        nome=nome,
        tipo=TipoUsuario.ALUNO,
        codigo_acesso=numero_matricula,
        foto_hash=img_encodings
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    novo_aluno = Aluno(
        id=novo_usuario.id,
        curso=curso
    )
    
    db.add(novo_aluno)
    db.commit()
    
    return UserResponse(
        id=novo_usuario.id,
        nome=nome,
        tipo=TipoUsuario.ALUNO,
        codigo_acesso=numero_matricula,
        curso=curso
    )
    

def registrar_professor(nome, numero_funcionario, departamento, image, db: Session) -> UserResponse:
    img_encodings = proccess_image(image)
    
    validar_encodings(img_encodings)
    if validar_usuario_existe(db, img_encodings):
        raise HTTPException(status_code=400, detail="Usuário já registrado.")

    img_encodings = json.dumps(img_encodings[0].tolist())
    
    novo_usuario = Usuario(
        nome=nome,
        tipo=TipoUsuario.PROFESSOR,
        codigo_acesso=numero_funcionario,
        foto_hash=img_encodings
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    novo_prof = Professor(
        id=novo_usuario.id,
        departamento=departamento
    )
    
    db.add(novo_prof)
    db.commit()
    
    return UserResponse(
        id=novo_usuario.id,
        nome=nome,
        tipo=TipoUsuario.PROFESSOR,
        codigo_acesso=numero_funcionario,
        departamento=departamento
    )
    

def registrar_administrador(nome, numero_funcionario, nivel, image, db: Session) -> UserResponse:
    img_encodings = proccess_image(image)
    
    validar_encodings(img_encodings)
    if validar_usuario_existe(db, img_encodings):
        raise HTTPException(status_code=400, detail="Usuário já registrado.")

    img_encodings = json.dumps(img_encodings[0].tolist())
    
    novo_usuario = Usuario(
        nome=nome,
        tipo=TipoUsuario.ADMIN,
        codigo_acesso=numero_funcionario,
        foto_hash=img_encodings
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    novo_adm = Administrador(
        id=novo_usuario.id,
        nivel=nivel
    )
    
    db.add(novo_adm)
    db.commit()
    
    return UserResponse(
        id=novo_usuario.id,
        nome=nome,
        tipo=TipoUsuario.ADMIN,
        codigo_acesso=numero_funcionario,
        nivel=nivel
    )

def validar_encodings(img_encodings):
    if not img_encodings:
        raise HTTPException(status_code=400, detail="Nenhum rosto detectado.")
    if len(img_encodings) > 1:
        raise HTTPException(status_code=400, detail="A imagem não pode conter mais de uma pessoa.")

def validar_usuario_existe(db: Session, img_encodings) -> bool:
    users = db.query(Usuario).all()
    
    for user in users:
        try:
            user_encodings = np.array(json.loads(user.foto_hash))
        except Exception:
            continue
        
        match = fr.compare_faces([user_encodings], img_encodings[0])
        
        if match[0]:
            return True
    return False