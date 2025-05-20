from datetime import datetime


def calcular_status_entrada(hora_inicio, entrada):
    diferenca = (datetime.combine(datetime.today(), entrada) - datetime.combine(datetime.today(), hora_inicio))
    minutos_atraso = diferenca.total_seconds() / 60
    
    if minutos_atraso <= 10:
        return 'pontual'
    elif minutos_atraso <= 30:
        return 'parcial'
    else:
        return 'fora_do_limite'