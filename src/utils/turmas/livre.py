import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.core.configs import UTANGA_API_URL

async def preparar_turma_livre(db: Session):
    id_turma = "EIMK_livre"
    id_cadeira = ""
    id_professor = 20151234  # valor placeholder, irrelevante pois não há aula

    turma_payload = {
        "id_turma": id_turma,
        "cadeiras": [
            {
                "id_cadeira": id_cadeira,
                "id_professor": id_professor
            }
        ],
        "horarios": [],
        "ids_estudantes": []
    }

    async with httpx.AsyncClient() as client:
        # ELIMINAR TURMA EXISTENTE
        await client.delete(f"{UTANGA_API_URL}turma/{id_turma}")

        # INSERIR NOVA TURMA
        response = await client.post(f"{UTANGA_API_URL}turma/", json=turma_payload)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Erro ao criar a turma livre: {response.text}"
            )
