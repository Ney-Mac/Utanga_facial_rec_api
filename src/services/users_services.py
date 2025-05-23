import json
import numpy as np
import face_recognition as fr
from datetime import datetime, time

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.Usuario import Usuario as User
from src.models.Dispensa import Dispensa as Disp

from src.db_models.usuario import Usuario
from src.db_models.controle_acesso import ControleAcesso

from src.utils.process_image import process_image, validar_encodings
from src.utils.calcular_status_entrada import calcular_status_entrada

import httpx
import http

from fastapi import HTTPException, status


UTANGA_API_URL = "http://localhost:8001/"


async def fazer_login(image, id_turma_destino: str, db: Session):
    img_encodings = process_image(image)
    validar_encodings(img_encodings)

    users = db.query(Usuario).all()
    
    for user in users:
        user_encodings = np.array(json.loads(user.face_encodings))
        match = fr.compare_faces([user_encodings], img_encodings[0], tolerance=0.45)

        if match[0]:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{UTANGA_API_URL}usuario/", params={"id": user.id})
                
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail="Erro na chamada da API ao tentar fazer login.")
                
                user_data_list = response.json()
                
                if not user_data_list:
                    raise HTTPException(status_code=404, detail="Usuário não encontrado na API.")
                
                user_data = user_data_list[0]
                tipo = user_data.get("tipo")

                if tipo == "adm":
                    return user_data
                elif tipo == "prof":
                    if not id_turma_destino:
                        raise HTTPException(status_code=400, detail="Turma de destino obrigatória para professores.")
                    return user_data
                elif tipo == "estudante":
                    if not id_turma_destino:
                        raise HTTPException(status_code=400, detail="Turma de destino obrigatória para estudantes.")
                    
                    turma = await buscar_turma_api(id_turma_destino)
                    em_aula, id_cadeira_em_aula = turma_em_aula(turma, datetime.now())
                    
                    if em_aula:
                        if aluno_na_turma(turma, user.id):
                            registrar_acesso(db, tipo="PERMITIDO", id_turma=id_turma_destino, id_cadeira=id_cadeira_em_aula, id_usuario=user.id)
                            return user_data
                        else:
                            registrar_acesso(db, tipo="BLOQUEADO", id_turma=id_turma_destino, id_cadeira=id_cadeira_em_aula, id_usuario=user.id)
                            raise HTTPException(status_code=401, detail="Aluno não autorizado para essa turma no momento.")
                    else:
                        registrar_acesso(db, tipo="PERMITIDO", id_turma=id_turma_destino, id_cadeira=0, id_usuario=user.id)
                        return user_data
                else:
                    raise HTTPException(status_code=400, detail="Tipo de usuário desconhecido.")
                
    raise HTTPException(status_code=400, detail="Usuario nao reconhecido.")
                

async def registrar_usuario(image, id_usuario: str, db: Session):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{UTANGA_API_URL}usuario/", params={"id": id_usuario})
        if not response:
            raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail="Usuário não existe.")
        
        user = response.json()
        
        img_encodings = process_image(image)
        validar_encodings(img_encodings)
        img_encodings = json.dumps(img_encodings[0].tolist())
        
        usuario = Usuario(id=id_usuario, face_encodings=img_encodings)
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        
        return {
            "message": f"Os dados faciais do usuário foram adicionados",
            "user": user
        }


async def listar_usuarios(tipo: str, id_usuario: str, db: Session):
    local_users = db.query(Usuario).all()
    local_ids = {user.id for user in local_users}
    # tipo = { "adm":"administrador", "prof":"professor", "estudante":"estudante" }.get(tipo)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{UTANGA_API_URL}usuario/", params={"id": id_usuario, "tipo": tipo})
        
        print(response.status_code)
        
        if response.status_code != 200:
            raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail="Usuário não existe.")
        
        users = response.json()

        for user in users:
            user_id = user.get("id")
            user["dados faciais"] = "sim" if user_id in local_ids else "nao"

        return users


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

async def buscar_usuario_api(id_usuario: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{UTANGA_API_URL}usuario/", params={"id": id_usuario})
    
    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail="Usuário não encontrado na API."
        )
    
    user_data_list = resp.json()
    
    if not user_data_list:  # Lista vazia = usuário não encontrado
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado na API (lista vazia)."
        )
    
    return user_data_list[0]  # Retorna o primeiro (e único) item


async def buscar_turma_api(id_turma: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{UTANGA_API_URL}turma/", params={"id": id_turma})
    
    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail="Turma não encontrada na API."
        )
    
    turmas = resp.json()  # Sempre uma lista de turmas
    
    # Filtra a lista para encontrar a turma com o ID especificado
    turma_encontrada = next((t for t in turmas if t["id"] == id_turma), None)
    
    if not turma_encontrada:
        raise HTTPException(
            status_code=404,
            detail=f"Turma com ID {id_turma} não encontrada na lista retornada."
        )
    
    return turma_encontrada  # Retorna um dicionário (não uma lista)

def turma_em_aula(turma: dict, agora: datetime):
    dia_map = {
        'mon': 'seg',
        'tue': 'ter',
        'wed': 'qua',
        'thu': 'qui',
        'fri': 'sex',
        'sat': 'sab',
        'sun': 'dom'
    }
    dia_atual = dia_map.get(agora.strftime('%a').lower())
    hora_atual = agora.time()

    for cadeira in turma.get("cadeiras", []):
        for horario in cadeira.get("horarios", []):
            if (horario["dia_semana"] == dia_atual and
                time.fromisoformat(horario["hora_inicio"]) <= hora_atual <= time.fromisoformat(horario["hora_fim"])):
                return True, cadeira["id"]
    return False, None

def aluno_na_turma(turma: dict, id_estudante: str):
    for cadeira in turma.get("cadeiras", []):
        for estudante in cadeira["estudantes"]:
            if estudante["id"] == id_estudante:
                return True
    return False

def registrar_acesso(db: Session, tipo: str, id_turma: str, id_cadeira: int, id_usuario: str):
    agora = datetime.now()
    acesso = ControleAcesso(
        data_criacao=agora.date(),
        hora_criacao=agora.time(),
        tipo=tipo,
        id_turma=int(id_turma),
        id_cadeira=id_cadeira,
        id_usuario=id_usuario
    )
    db.add(acesso)
    db.commit()
