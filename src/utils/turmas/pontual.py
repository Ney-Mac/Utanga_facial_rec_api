import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.usuario import TableUsuario
from src.core.configs import UTANGA_API_URL


async def preparar_turma_pontual(db: Session):
    from datetime import datetime, timedelta
    
    id_turma = "EIMK_pontual"
    id_cadeira = "Matematica"
    id_professor = 20151234
    
    # Mapear dia da semana
    dias_semana_map = {
        0: "SEG",
        1: "TER",
        2: "QUA",
        3: "QUI",
        4: "SEX",
        5: "SAB",
        6: "DOM"
    }
    
    data_hora_atual = datetime.now()
    dia_atual = dias_semana_map[data_hora_atual.weekday()]
    
    hora_inicio = (data_hora_atual - timedelta(minutes=14)).time().strftime("%H:%M:%S")
    hora_fim = (data_hora_atual + timedelta(hours=2)).time().strftime("%H:%M:%S")

    # Buscar todos os estudantes cadastrados
    estudantes = db.query(TableUsuario).all()
    ids_estudantes = [e.id for e in estudantes]

    turma_payload = {
        "id_turma": id_turma,
        "cadeiras": [
            {
                "id_cadeira": id_cadeira,
                "id_professor": id_professor
            }
        ],
        "horarios": [
            {
                "id_cadeira": id_cadeira,
                "dia_semana": dia_atual,
                "hora_inicio": hora_inicio,
                "hora_fim": hora_fim
            }
        ],
        "ids_estudantes": ids_estudantes
    }

    async with httpx.AsyncClient() as client:
        # REMOVER TURMA EXISTENTE (fictício por enquanto)
        await client.delete(f"{UTANGA_API_URL}turma/{id_turma}")
        
        # INSERIR NOVA TURMA
        response = await client.post(f"{UTANGA_API_URL}turma/", json=turma_payload)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Erro ao criar a turma pontual."
            )
