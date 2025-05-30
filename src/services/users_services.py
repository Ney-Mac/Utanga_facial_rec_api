import http
import json
import httpx
import numpy as np
import face_recognition as fr
from datetime import datetime, timedelta
from fastapi import HTTPException, responses
from sqlalchemy.orm import Session

from src.entities.Usuario import Usuario
from src.entities.ControleAcesso import ControleAcesso
from src.utils.tipo_acesso import TipoAcesso

from src.models.usuario import TableUsuario

from fastapi import HTTPException
from src.core.configs import UTANGA_API_URL

from src.utils.turmas.pontual import preparar_turma_pontual
from src.utils.turmas.parcial import preparar_turma_parcial
from src.utils.turmas.total import preparar_turma_total
from src.utils.turmas.livre import preparar_turma_livre


def registrar_acesso(db, tipo: str, data_hora_atual: datetime, id_usuario: str = None, id_turma: str ="", id_cadeira: str =""):
    novo_acesso = ControleAcesso(
        data_criacao=data_hora_atual.date(),
        hora_criacao=data_hora_atual.time(),
        tipo=tipo,
        id_turma=id_turma,
        id_cadeira=id_cadeira,
        id_usuario=id_usuario
    )
    try:
        novo_acesso.registrar_entrada(db)
    except Exception as e:
        print(f"Erro ao registar acesso.")

async def fazer_login(image, id_turma_destino: str, db: Session):
    dados_faciais = Usuario.fazer_reconhecimento(image)
    users = db.query(TableUsuario).all()

    # Definir data/hora e dia atual logo no começo da função
    agora = datetime.now()
    dias_semana_map = ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"]
    dia_atual = dias_semana_map[agora.weekday()]
    hora_atual = agora.time()

    for user in users:
        dados_faciais_salvos = np.array(json.loads(user.face_encodings))
        match = fr.compare_faces([dados_faciais_salvos], dados_faciais, tolerance=0.45)

        if match[0]:
            # Preparar turma se necessário
            if id_turma_destino == "EIMK_pontual":
                await preparar_turma_pontual(db)
            elif id_turma_destino == "EIMK_parcial":
                await preparar_turma_parcial(db)
            elif id_turma_destino == "EIMK_total":
                await preparar_turma_total(db)
            elif id_turma_destino == "EIMK_livre":
                await preparar_turma_livre(db)

            async with httpx.AsyncClient() as client:
                # Buscar dados do usuário
                response = await client.get(f"{UTANGA_API_URL}usuario/", params={"id": user.id})
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail="Erro ao buscar usuário.")

                user_data_list = response.json()
                if not user_data_list:
                    raise HTTPException(status_code=404, detail="Usuário não encontrado.")
                user_data = user_data_list[0]

                # Buscar horários da turma (1 única vez)
                response_horarios = await client.get(f"{UTANGA_API_URL}horarios/", params={"id_turma": id_turma_destino})
                if response_horarios.status_code != 200:
                    raise HTTPException(status_code=500, detail="Erro ao buscar horários da turma.")
                horarios = response_horarios.json()

                aula_em_andamento = None
                for horario in horarios:
                    if horario["dia_semana"] != dia_atual:
                        continue
                    hora_inicio = datetime.strptime(horario["hora_inicio"], "%H:%M:%S").time()
                    hora_fim = datetime.strptime(horario["hora_fim"], "%H:%M:%S").time()
                    if hora_inicio <= hora_atual <= hora_fim:
                        aula_em_andamento = {
                            "id_cadeira": horario["id_cadeira"],
                            "hora_inicio": hora_inicio
                        }
                        break

                # Se NÃO houver aula em andamento, permitir acesso como "turma livre"
                if not aula_em_andamento:
                    registrar_acesso(
                        db=db,
                        tipo=TipoAcesso.ACEITE,
                        data_hora_atual=agora,
                        id_usuario=user_data["id"],
                        id_cadeira="",
                        id_turma=id_turma_destino
                    )
                    return responses.JSONResponse(
                        status_code=200,
                        content={
                            "message": f"Acesso concedido. Utilize a turma para adiquirir conhecimento, estudante {user_data['nome']}.",
                            "user": {
                                "id": user_data["id"],
                                "nome": user_data["nome"],
                                "ano_lectivo": user_data["ano_lectivo"],
                                "curso": user_data["curso"],
                                "tipo": user_data["tipo"]
                            }
                        }
                    )

                # Buscar cadeiras e turmas do estudante
                response_cadeira_turma = await client.get(f"{UTANGA_API_URL}estudante-cadeiras/{user_data['id']}")
                if response_cadeira_turma.status_code != 200:
                    raise HTTPException(status_code=500, detail="Erro ao buscar cadeira-turma do estudante.")
                lista_cadeiras_turmas = response_cadeira_turma.json()

                # Se houver aula em andamento, validar inscrição
                if aula_em_andamento:
                    inscrito = any(
                        ct["id_cadeira"] == aula_em_andamento["id_cadeira"] and ct["id_turma"] == id_turma_destino
                        for ct in lista_cadeiras_turmas
                    )
                    if not inscrito:
                        registrar_acesso(
                            db=db,
                            tipo=TipoAcesso.REJEITADO,
                            data_hora_atual=agora,
                            id_usuario=user_data["id"],
                            id_cadeira=aula_em_andamento["id_cadeira"],
                            id_turma=id_turma_destino
                        )
                        return responses.JSONResponse(
                            status_code=200,
                            content={
                                "message": "Acesso negado - você não está inscrito na cadeira em aula.",
                                "acesso_especial_disponivel": "nao",
                                "user": {
                                    "id": user_data["id"],
                                    "nome": user_data["nome"],
                                    "ano_lectivo": user_data["ano_lectivo"],
                                    "curso": user_data["curso"],
                                    "tipo": user_data["tipo"]
                                }
                            }
                        )

                    # Calcular atraso
                    hora_inicio_dt = datetime.combine(agora.date(), aula_em_andamento["hora_inicio"])
                    atraso = agora - hora_inicio_dt

                    if atraso > timedelta(minutes=40):
                        registrar_acesso(
                            db=db,
                            tipo=TipoAcesso.REJEITADO,
                            data_hora_atual=agora,
                            id_usuario=user_data["id"],
                            id_cadeira=aula_em_andamento["id_cadeira"],
                            id_turma=id_turma_destino
                        )
                        return responses.JSONResponse(
                            status_code=200,
                            content={
                                "message": f"Atraso superior a 40 minutos - entrada não permitida, estudante {user_data['nome']}.",
                                "acesso_especial_disponivel": "nao",
                                "user": {
                                    "id": user_data["id"],
                                    "nome": user_data["nome"],
                                    "ano_lectivo": user_data["ano_lectivo"],
                                    "curso": user_data["curso"],
                                    "tipo": user_data["tipo"]
                                }
                            }
                        )
                    elif atraso > timedelta(minutes=15):
                        registrar_acesso(
                            db=db,
                            tipo=TipoAcesso.REJEITADO,
                            data_hora_atual=agora,
                            id_usuario=user_data["id"],
                            id_cadeira=aula_em_andamento["id_cadeira"],
                            id_turma=id_turma_destino
                        )
                        return responses.JSONResponse(
                            status_code=200,
                            content={
                                "message": f"Atraso superior a 15 minutos - entrada não permitida, estudante {user_data['nome']}.",
                                "acesso_especial_disponivel": "sim",
                                "user": {
                                    "id": user_data["id"],
                                    "nome": user_data["nome"],
                                    "ano_lectivo": user_data["ano_lectivo"],
                                    "curso": user_data["curso"],
                                    "tipo": user_data["tipo"]
                                }
                            }
                        )
                    else:
                        registrar_acesso(
                            db=db,
                            tipo=TipoAcesso.ACEITE,
                            data_hora_atual=agora,
                            id_usuario=user_data["id"],
                            id_cadeira=aula_em_andamento["id_cadeira"],
                            id_turma=id_turma_destino
                        )
                        return responses.JSONResponse(
                            status_code=200,
                            content={
                                "message": f"Acesso concedido. Tenha um excelente aproveitamento, estudante {user_data['nome']}.",
                                "user": {
                                    "id": user_data["id"],
                                    "nome": user_data["nome"],
                                    "ano_lectivo": user_data["ano_lectivo"],
                                    "curso": user_data["curso"],
                                    "tipo": user_data["tipo"]
                                }
                            }
                        )

                # Caso a turma não esteja em aula, permitir acesso
                registrar_acesso(
                    db=db,
                    tipo=TipoAcesso.ACEITE,
                    data_hora_atual=agora,
                    id_usuario=user_data["id"],
                    id_turma=id_turma_destino
                )
                return responses.JSONResponse(
                    status_code=200,
                    content={
                        "message": f"Acesso concedido. Tenha um excelente aproveitamento, estudante {user_data['nome']}.",
                        "user": {
                            "id": user_data["id"],
                            "nome": user_data["nome"],
                            "ano_lectivo": user_data["ano_lectivo"],
                            "curso": user_data["curso"],
                            "tipo": user_data["tipo"]
                        }
                    }
                )

    # Se ninguém for reconhecido
    registrar_acesso(db=db, tipo=TipoAcesso.REJEITADO, data_hora_atual=datetime.now())
    raise HTTPException(status_code=400, detail="Usuário não reconhecido.")


async def registrar_usuario(image, id_usuario: str, db: Session):
    usuario_existente = db.query(TableUsuario).filter_by(id=id_usuario).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Usuário já está cadastrado.")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{UTANGA_API_URL}usuario/", params={"id": id_usuario})
        if not response:
            raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail="Usuário não existe.")
        
        user = response.json()
        
        dados_faciais = Usuario.fazer_reconhecimento(image)
        dados_faciais_json = json.dumps(dados_faciais.tolist())
        
        usuario = TableUsuario(id=id_usuario, face_encodings=dados_faciais_json)
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        
        return {
            "message": f"Os dados faciais do usuário foram adicionados",
            "user": user
        }


async def listar_usuarios(tipo: str, id_usuario: str, db: Session):
    local_users = db.query(TableUsuario).all()
    local_ids = {user.id for user in local_users}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{UTANGA_API_URL}usuario/", params={"id": id_usuario, "tipo": tipo})
        
        if response.status_code != 200:
            raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail="Usuário não existe.")
        
        users = response.json()

        for user in users:
            user_id = user.get("id")
            user["dados faciais"] = "sim" if user_id in local_ids else "nao"

        return users
