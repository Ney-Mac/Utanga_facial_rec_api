import httpx
from fastapi import HTTPException
from src.core.configs import UTANGA_API_URL


async def buscar_turma_api(id_turma: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{UTANGA_API_URL}turma/", params={"id": id_turma})
    
    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail="Turma não encontrada na API."
        )
    
    turmas = resp.json()
    return turmas[0]