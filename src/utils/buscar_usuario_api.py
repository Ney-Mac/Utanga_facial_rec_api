import httpx
from fastapi import HTTPException
from src.core.configs import UTANGA_API_URL


async def buscar_usuario_api(id_usuario: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{UTANGA_API_URL}usuario/", params={"id": id_usuario})
    
    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail="Usuário não encontrado na API."
        )
    
    user_data_list = resp.json()
    
    if not user_data_list:  # Lista vazia = usuário não encontrado
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado na API."
        )
    
    return user_data_list[0]  # Retorna o primeiro (e único) item
