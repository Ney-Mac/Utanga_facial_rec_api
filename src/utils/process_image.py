import face_recognition as fr
import cv2
from io import BytesIO
from fastapi import HTTPException


def process_image(image):
    img_loaded = fr.load_image_file(BytesIO(image))
    img_loaded = cv2.cvtColor(img_loaded, cv2.COLOR_BGR2RGB)
    return fr.face_encodings(img_loaded)

def validar_encodings(img_encodings):
    if not img_encodings:
        raise HTTPException(status_code=400, detail="Nenhum rosto detectado.")
    if len(img_encodings) > 1:
        raise HTTPException(
            status_code=400, detail="A imagem não pode conter mais de uma pessoa.")
