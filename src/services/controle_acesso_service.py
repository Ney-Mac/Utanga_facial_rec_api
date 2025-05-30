import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from src.models.controle_acesso import TableControleAcesso
from src.utils.tipo_acesso import TipoAcesso
from src.services.users_services import listar_usuarios
from src.core.configs import UTANGA_API_URL


async def buscar_acesso(db: Session, tipo: Optional[TipoAcesso] = None):
    acessos_query = db.query(TableControleAcesso)
    
    if tipo:
        acessos_query = acessos_query.filter_by(tipo=tipo.value)
    
    acessos_query_all = acessos_query.all()
    
    if not acessos_query_all:
        raise HTTPException(status_code=404, detail="Nenhum acesso encontrado.")
    
    acessos_resultado = []
    
    async with httpx.AsyncClient() as client:
        for acesso in acessos_query_all:
            nome_estudante = ""
            n_matricula = ""
            turma_nome = ""

            # Buscar usuário se houver ID
            if acesso.id_usuario:
                try:
                    resp_user = await client.get(
                        f"{UTANGA_API_URL}usuario/",
                        params={"id": acesso.id_usuario}
                    )
                    if resp_user.status_code == 200:
                        usuarios = resp_user.json()
                        if usuarios:
                            usuario = usuarios[0]  # Supondo que vem em lista
                            nome_estudante = usuario.get("nome", "")
                            n_matricula = str(usuario.get("id", ""))
                except Exception as e:
                    print(f"Erro ao buscar usuário {acesso.id_usuario}: {e}")

            # Buscar turma se houver ID
            if acesso.id_turma:
                try:
                    resp_turma = await client.get(
                        f"{UTANGA_API_URL}turma/",
                        params={"id": acesso.id_turma}
                    )
                    if resp_turma.status_code == 200:
                        turmas = resp_turma.json()
                        if turmas:
                            turma_nome = turmas[0].get("id", "")
                except Exception as e:
                    print(f"Erro ao buscar turma {acesso.id_turma}: {e}")

            acessos_resultado.append({
                "nome_estudante": nome_estudante,
                "n_matricula": n_matricula,
                "turma": turma_nome,
                "hora_entrada": acesso.hora_criacao.strftime("%H:%M:%S"),
                "data_entrada": acesso.data_criacao.strftime("%Y-%m-%d"),
                "estado": acesso.tipo
            })

    return acessos_resultado

async def buscar_acessos_por_turma(id_turma: str, db: Session):
    acessos_query = db.query(TableControleAcesso).filter_by(id_turma=id_turma)
    acessos_query_all = acessos_query.all()

    if not acessos_query_all:
        raise HTTPException(status_code=404, detail="Nenhum acesso encontrado para essa turma.")

    # Buscar dados da turma pela API externa
    async with httpx.AsyncClient() as client:
        turma_response = await client.get(f"{UTANGA_API_URL}turma/", params={"id": id_turma})
        if turma_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Turma não encontrada.")

        turma_data = turma_response.json()
        cadeiras_info = turma_data[0].get("cadeiras", [])  # Assume 1 turma

    acessos_resultado = []

    for acesso in acessos_query_all:
        if not acesso.id_usuario:
            continue  # Ignorar se o acesso não tiver usuário

        # Buscar info do usuário
        users = await listar_usuarios("estudante", acesso.id_usuario, db)
        usuario = next((u for u in users if str(u["id"]) == str(acesso.id_usuario)), None)
        if not usuario:
            continue

        # Obter nome da cadeira (via id_cadeira no acesso)
        cadeira_nome = next(
            (c["id"] for c in cadeiras_info if c["id"] == acesso.id_cadeira),
            acesso.id_cadeira  # fallback
        )

        acessos_resultado.append({
            "nome_estudante": usuario.get("nome", ""),
            "n_matricula": str(usuario.get("id", "")),
            "hora_entrada": acesso.hora_criacao.strftime("%H:%M:%S"),
            "data_entrada": acesso.data_criacao.strftime("%Y-%m-%d"),
            "estado": acesso.tipo,
            "cadeira": cadeira_nome
        })

    return {
        "id_turma": id_turma,
        "acessos": acessos_resultado
    }
