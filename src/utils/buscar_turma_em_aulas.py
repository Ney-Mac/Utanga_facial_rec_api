from datetime import datetime, time


def turma_em_aula(turma: dict, agora: datetime):
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
            if (horario["dia_semana"] == dia_atual and
                time.fromisoformat(horario["hora_inicio"]) <= hora_atual <= time.fromisoformat(horario["hora_fim"])):
                return True, cadeira["id"]
    return False, None
