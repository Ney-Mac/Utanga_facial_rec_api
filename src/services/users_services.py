import json
import numpy as np
import face_recognition as fr
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.Usuario import Usuario as User
from src.models.Dispensa import Dispensa as Disp

from src.db_models.Usuario import Usuario
from src.db_models.Turma import Turma
from src.db_models.Cadeira import Cadeira
from src.db_models.Dispensa import Dispensa
from src.db_models.Controle_Acesso import Controle_Acesso

from src.utils.process_image import process_image, validar_encodings
from src.utils.calcular_status_entrada import calcular_status_entrada


def fazer_login(image, id_turma_destino: str, db: Session):
    img_encodings = process_image(image)
    validar_encodings(img_encodings)

    users = db.query(Usuario).all()

    for user in users:
        user_encodings = np.array(json.loads(user.foto_hash))
        match = fr.compare_faces([user_encodings], img_encodings[0], tolerance=0.45)

        if match[0]:
            if user.tipo == 'adm':  # Logar administrador
                return {
                    "id_usuario": user.id_usuario,
                    "nome": user.nome,
                    "tipo": user.tipo,
                    "matricula": None,
                    "ano_letivo": None,
                    "curso": None,
                    "turma": None
                }
            
            if not id_turma_destino:
                raise HTTPException(status_code=400, detail="Turma de destino obrigatória para alunos e professores.")
            else:
                turma = db.query(Turma).filter_by(id_turma=id_turma_destino).first()
                if not turma:
                    raise HTTPException(status_code=400, detail="Turma não existe!")

                if user.tipo == "prof":  # Permitir acesso do prof na turma
                    return {
                        "id_usuario": user.id_usuario,
                        "nome": user.nome,
                        "tipo": user.tipo,
                        "matricula": None,
                        "ano_letivo": None,
                        "curso": None,
                        "turma": user.id_turma
                        # "turma_destino": id_turma_destino
                    }
                    
                else: #  Verificacoes para acesso do aluno
                    #  Verificar se a turma esta em aulas
                    agora = datetime.now()
                    hora_atual = datetime.strptime("20:15", "%H:%M").time()
                    # hora_atual = agora.time()

                    dia_map = {
                        'mon': 'seg',
                        'tue': 'ter',
                        'wed': 'qua',
                        'thu': 'qui',
                        'fri': 'sex',
                        'sat': 'sab',
                        'sun': 'dom'
                    }

                    # dia_atual = dia_map.get(agora.strftime('%a').lower(), '')
                    dia_atual = 'sex'

                    for cadeira in turma.cadeiras:
                        for horario in cadeira.horarios:
                            if horario.dia == dia_atual and horario.hora_inicio <= hora_atual <= horario.hora_fim:  # Retorna True se Turma em aulas
                                #  Se estiver em aulas, verificar se o aluno esta autorizado a entrar (pertence a turma e nao esta dispensado)
                                usuario = User(
                                    id=user.id_usuario,
                                    nome=user.nome,
                                    matricula=user.matricula,
                                    dados_face=user.foto_hash,
                                    ano_lectivo=user.ano_lectivo,
                                    curso=user.curso,
                                    id_turma=user.id_turma,
                                    tipo='aluno'
                                )
                                
                                # disp = cadeira.dispensas  # retorna todas as dispensas desta cadeira nesta turma
                                
                                disp = next(
                                    (d for d in cadeira.dispensas if d.id_usuario == user.id_usuario),
                                    None
                                )
                                
                                if not disp:
                                    #  Se nao esta dispensado, permitir acesso e marcar presenca
                                    status = calcular_status_entrada(horario.hora_inicio, hora_atual)
                                    
                                    novo_acesso = Controle_Acesso(
                                        data_hora_entrada=agora,
                                        status_entrada=status,
                                        acesso_especial=False,
                                        id_usuario=usuario.id,
                                        id_turma_acessada=id_turma_destino
                                    )
                                    
                                    db.add(novo_acesso)
                                    db.commit()
                                    
                                    return {
                                        "id_usuario": user.id_usuario,
                                        "nome": user.nome,
                                        "tipo": user.tipo,
                                        "matricula": user.matricula,
                                        "ano_letivo": user.ano_letivo,
                                        "curso": user.curso,
                                        "turma": user.id_turma
                                        # "turma_destino": id_turma_destino
                                    }
                                
                                dispensa = Disp(
                                    id=disp.id,
                                    nota_p1=disp.nota_p1,
                                    nota_p2=disp.nota_p2,
                                    id_cadeira=disp.id_cadeira
                                )
                                
                                if usuario.verificar_dispensa(dispensa):
                                    raise HTTPException(status_code=401, detail="Aluno dispensado.")
                                else:
                                    #  Se nao esta dispensado, permitir acesso e marcar presenca
                                    status = calcular_status_entrada(horario.hora_inicio, hora_atual)
                                    
                                    novo_acesso = Controle_Acesso(
                                        data_hora_entrada=agora,
                                        status_entrada=status,
                                        acesso_especial=False,
                                        id_usuario=usuario.id,
                                        id_turma_acessada=id_turma_destino
                                    )
                                    
                                    db.add(novo_acesso)
                                    db.commit()
                                    
                                    return {
                                        "id_usuario": user.id_usuario,
                                        "nome": user.nome,
                                        "tipo": user.tipo,
                                        "matricula": user.matricula,
                                        "ano_letivo": user.ano_letivo,
                                        "curso": user.curso,
                                        "turma": user.id_turma
                                        # "turma_destino": id_turma_destino
                                    }
                                    
    raise HTTPException(status_code=401, detail="Usuário não reconhecido.")


def listar_usuarios(tipo: str, id_usuario: int, db: Session):
    filtros = []

    if tipo:
        filtros.append(Usuario.tipo == tipo)

    if id_usuario:
        filtros.append(Usuario.id_usuario == id_usuario)

    usuarios = db.query(Usuario).filter(*filtros).all()

    if usuarios:
        return [
            {
                "id_usuario": usuario.id_usuario,
                "nome": usuario.nome,
                "tipo": usuario.tipo,
                "matricula": usuario.matricula,
                "ano_letivo": usuario.ano_letivo,
                "curso": usuario.curso,
                "turma": usuario.id_turma
            }
            for usuario in usuarios
        ]
    else:
        raise HTTPException(
            status_code=404, detail="Nenhum usuário encontrado.")


def registrar_usuario(
        image,
        db: Session,
        tipo: str,
        id_turma: int,
        nome: str,
        matricula: str = None,
        ano_letivo: str = None,
        curso: str = None
    ):
    
    img_encodings = process_image(image)
    validar_encodings(img_encodings)
    
    if validar_usuario_existe(db, img_encodings):
        raise HTTPException(status_code=400, detail="Usuário já registrado.")

    if tipo == 'adm':
        id_turma: int = 1
    else:
        turma = db.query(Turma).filter_by(id_turma=id_turma).first()
        if not turma:
            raise HTTPException(status_code=400, detail="Turma inexistente.")

    img_encodings = json.dumps(img_encodings[0].tolist())

    novo_usuario = Usuario(
        nome=nome,
        tipo=tipo,
        id_turma=id_turma,
        matricula=matricula,
        ano_letivo=ano_letivo,
        curso=curso,
        foto_hash=img_encodings
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    if tipo == 'adm':
        return {
            "id_usuario": novo_usuario.id_usuario,
            "nome": novo_usuario.nome,
            "tipo": novo_usuario.tipo,
            "matricula": None,
            "ano_letivo": None,
            "curso": None,
            "turma": None
        }
    elif tipo == "prof":
        return {
            "id_usuario": novo_usuario.id_usuario,
            "nome": novo_usuario.nome,
            "tipo": novo_usuario.tipo,
            "matricula": None,
            "ano_letivo": None,
            "curso": None,
            "turma": novo_usuario.id_turma
        }
    else:
        return {
            "id_usuario": novo_usuario.id_usuario,
            "nome": novo_usuario.nome,
            "tipo": novo_usuario.tipo,
            "matricula": None,
            "ano_letivo": None,
            "curso": None,
            "turma": novo_usuario.id_turma
        }


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
