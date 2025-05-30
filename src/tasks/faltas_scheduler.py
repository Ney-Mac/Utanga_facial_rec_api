import httpx
from sqlalchemy.orm import Session
from datetime import date
from apscheduler.schedulers.background import BackgroundScheduler
from src.core.configs import UTANGA_API_URL
from src.models.controle_acesso import TableControleAcesso
from src.core.database import SessionLocal
from src.utils.tipo_acesso import TipoAcesso


scheduler = BackgroundScheduler()


def marcar_faltas():
    db: Session = SessionLocal()
    hoje = date.today()
    dia_semana = ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"][hoje.weekday()]

    try:
        with httpx.Client() as client:
            # 1. Buscar todas as turmas
            turmas_response = client.get(f"{UTANGA_API_URL}turma/")
            turmas_response.raise_for_status()
            turmas = turmas_response.json()
            
            for turma in turmas:
                id_turma = turma["id"]

                for cadeira in turma["cadeiras"]:
                    id_cadeira = cadeira["id"]

                    # 3. Buscar horários dessa cadeira
                    response_horarios = client.get(f"{UTANGA_API_URL}horarios/", params={
                        "id_turma": id_turma,
                        "id_cadeira": id_cadeira
                    })
                    response_horarios.raise_for_status()
                    horarios = response_horarios.json()

                    for horario in horarios:
                        if horario["dia_semana"] != dia_semana:
                            continue

                        estudantes = cadeira["estudantes"]

                        # 5. Buscar acessos PERMITIDO hoje para a cadeira/turma
                        acessos = db.query(TableControleAcesso).filter(
                            TableControleAcesso.tipo == TipoAcesso.ACEITE.value,
                            TableControleAcesso.id_turma == id_turma,
                            TableControleAcesso.id_cadeira == id_cadeira,
                            TableControleAcesso.data_criacao == hoje
                        ).all()

                        ids_presentes = {acesso.id_usuario for acesso in acessos}

                        # 6. Marcar falta para quem não compareceu
                        for estudante in estudantes:
                            id_estudante = estudante["id"]
                            if id_estudante not in ids_presentes:
                                try:
                                    print(f"Marcando falta: estudante {id_estudante} - {id_turma}/{id_cadeira}")
                                    client.post(f"{UTANGA_API_URL}faltas/", json={
                                        "id_estudante": id_estudante,
                                        "id_cadeira": id_cadeira,
                                        "id_turma": id_turma,
                                        "id_horario": horario["id"]
                                    })
                                except Exception as e:
                                    print(f"Erro ao marcar falta para {id_estudante}: {e}")

    except Exception as e:
        print(f"Erro geral ao marcar faltas: {e}")
    finally:
        db.close()


def iniciar_agendamentos():
    scheduler.add_job(marcar_faltas, 'cron', hour=19, minute=53, day_of_week='mon-sat')
    scheduler.start()