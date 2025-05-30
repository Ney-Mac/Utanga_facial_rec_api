import json
import numpy as np
import face_recognition as fr
from sqlalchemy.orm import Session
from src.models.usuario import TableUsuario


def validar_usuario_existe(db: Session, img_encodings) -> bool:
    users = db.query(TableUsuario).all()

    for user in users:
        try:
            user_encodings = np.array(json.loads(user.face_encodings))
        except Exception:
            continue

        match = fr.compare_faces([user_encodings], img_encodings[0])

        if match[0]:
            return True
    return False