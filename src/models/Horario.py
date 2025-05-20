from datetime import date


class Horario:
    def __init__(self, id_turma: int, id_cadeira: int, dia_semana: str, hora_inicio: date, hora_fim: date):
        self.id_turma = id_turma
        self.id_cadeira = id_cadeira
        self.dia_semana = dia_semana
        self.hora_inicio = hora_fim
        self.hora_fim = hora_fim
        
    def ver_horario(self):
        return f"Turma: {self.id_turma} | Cadeira: {self.id_cadeira} | {self.dia_semana} - {self.hora_inicio}:{self.hora_fim}"
    