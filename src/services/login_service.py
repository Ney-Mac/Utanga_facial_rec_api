import json
import numpy as np
import face_recognition as fr
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.db_models.Usuario import Usuario
from src.db_models.Turma import Turma
from src.db_models.Cadeira import Cadeira

from utils.process_image import process_image


from src.utils.function import verificar_turma_em_aula, verificar_dispensa, marcar_presenca


def fazer_login(image, id_turma_destino: str, db: Session):
    turma = db.query(Turma).filter_by(id_turma=id_turma_destino).first()
    if not turma:
        raise HTTPException(
            status_code=400,
            detail="Turma não existe!"
        )

    img_encodings = process_image(image)

    if not img_encodings:
        raise HTTPException(status_code=400, detail="Nenhum rosto detectado.")
    if len(img_encodings) > 1:
        raise HTTPException(
            status_code=400, detail="A imagem não pode conter mais de uma pessoa.")

    users = db.query(Usuario).all()

    for user in users:  # Pesquisa usuario na BD
        try:
            user_encodings = np.array(json.loads(user.foto_hash))
        except Exception:
            continue

        match = fr.compare_faces(
            [user_encodings], img_encodings[0], tolerance=0.45)

        if match[0]:
            #  Verificar se a turma esta em aulas
            em_aulas = verificar_turma_em_aula(turma)
            
            #  Se estiver em aulas, verificar se o aluno esta autorizado a entrar (pertence a turma e nao esta dispensado)
            if em_aulas:
                cadeira = db.query(Cadeira).filter_by(id_cadeira=em_aulas["nome_cadeira"]).first()
                
                dispensado = verificar_dispensa(
                    turma=turma,
                    cadeira=cadeira,
                    usuario=user,
                    db=db
                )
                
                #  Se nao esta autorizado, negar acesso
                if dispensado:
                    raise HTTPException(status_code=400, detail="Aluno dispensado.")

                #  Se nao esta dispensado, permitir acesso e marcar presenca
                presenca = marcar_presenca(
                    db=db,
                    id_usuario=user.id_usuario,
                    id_turma=turma.id_turma,
                    hora_inicio=em_aulas["hora_inicio"]
                )
                
                if presenca:
                    print("Marcada")

            #  Se nao esta em aulas, permitir acesso
            #  Se esta autorizado, permitir acesso
            
            return {
                "id": user.id_usuario,
            }

    raise HTTPException(status_code=401, detail="Usuário não reconhecido.")
