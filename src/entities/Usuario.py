import face_recognition as fr
import numpy as np
import cv2
from io import BytesIO
from fastapi import HTTPException


class Usuario:
    def __init__(self, nome, matricula, ano_lectivo, curso):
        self.nome = nome
        self.matricula = matricula
        self.ano_lectivo = ano_lectivo
        self.curso = curso

    def solicitar_acesso_especial(self):
        pass

    def verificar_dispensa(self):
        pass

    @staticmethod
    def fazer_reconhecimento(image):
        # Extracao da imagem e codificacao da face
        img_carregada = fr.load_image_file(BytesIO(image))
        img_carregada = cv2.cvtColor(img_carregada, cv2.COLOR_BGR2RGB)
        
        codificacoes_da_face = fr.face_encodings(img_carregada)
        
        # Validacao do numero de pessoas detectadas na imagem
        if not codificacoes_da_face:    
            raise HTTPException(status_code=404, detail="Nenhum rosto detectado.")
        if len(codificacoes_da_face) > 1:
            raise HTTPException(status_code=400, detail="A imagem não pode conter mais de uma pessoa.")

        return codificacoes_da_face[0] # rotorna os dados facias
