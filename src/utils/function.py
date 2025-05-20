from src.db_models.Turma import Turma
from src.db_models.Cadeira import Cadeira
from src.db_models.Usuario import Usuario
from src.db_models.Nota import Nota
from src.db_models.Controle_Acesso import Controle_Acesso

from datetime import datetime
from sqlalchemy.orm import Session


def calcular_status_entrada(hora_inicio, entrada):
    diferenca = (datetime.combine(datetime.today(), entrada) - datetime.combine(datetime.today(), hora_inicio))
    minutos_atraso = diferenca.total_seconds() / 60
    
    if minutos_atraso <= 10:
        return 'pontual'
    elif minutos_atraso <= 30:
        return 'parcial'
    else:
        return 'fora_do_limite'

def marcar_presenca(db: Session, id_usuario: int, id_turma: int, hora_inicio, acesso_especial: bool = False):
    agora = datetime.now()
    entrada = agora.time()
    
    status = calcular_status_entrada(hora_inicio, entrada)
    
    novo_acesso = Controle_Acesso(
        data_hora_entrada=agora,
        status_entrada=status,
        acesso_especial=acesso_especial,
        id_usuario=id_usuario,
        id_turma_acessada=id_turma
    )
    
    db.add(novo_acesso)
    db.commit()
    
    return novo_acesso

def verificar_dispensa(turma: Turma, cadeira: Cadeira, usuario: Usuario, db: Session):
    nota = db.query(Nota).filter_by(
        id_usuario=usuario.id_usuario,
        id_turma=turma.id_turma,
        id_cadeira=cadeira.id_cadeira
    ).first()

    if nota:
        media = (nota.nota_p1 + nota.nota_p2)/2
        if media >= 14:
            return True
        
    return False   

def verificar_turma_em_aula(turma: Turma):
    horarios = turma.horarios
    agora = datetime.now()

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
    # hora_atual = agora.time()
    dia_atual = 'sex'
    hora_atual = datetime.strptime("20:15", "%H:%M").time()

    for horario in horarios:
        if horario.dia == dia_atual:
            if horario.hora_inicio <= hora_atual <= horario.hora_fim:
                return {
                    "nome_cadeira": horario.id_cadeira,
                    "hora_inicio": horario.hora_inicio
                }

    return None
