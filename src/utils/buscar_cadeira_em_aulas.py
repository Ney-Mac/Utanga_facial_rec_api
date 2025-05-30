import httpx
from datetime import datetime, time
from src.core.configs import UTANGA_API_URL
from .buscar_turma_api import buscar_turma_api

async def buscar_cadeira_em_aulas(id_turma: str, agora: datetime):
    turma = await buscar_turma_api(id_turma)
    
    dia_map = {
        'mon': 'seg',
        'tue': 'ter',
        'wed': 'qua',
        'thu': 'qui',
        'fri': 'sex',
        'sat': 'sab',
        'sun': 'dom'
    }
    dia_atual = dia_map.get(agora.strftime('%a').lower())
    hora_atual = agora.time()
    
    for cadeira in turma.get("cadeiras", []):        
        for horario in cadeira.get("horarios", []):
            if (horario["dia_semana"] == dia_atual and time.fromisoformat(horario["hora_inicio"]) <= hora_atual <= time.fromisoformat(horario["hora_fim"])):
                return cadeira["id"]