from src.utils.DiaSemana import DiaSemana
from datetime import time


class Turma:
    def __init__(self, codigo_turma: str, sala: str, dia_semana: DiaSemana, hora_inicio: time, hora_fim: time):
        self.codigo_turma = codigo_turma
        self.sala = sala
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim

    def listarAlunos(self):
        return "Listar alunos"

    def listarProvas(self):
        return "Listar provas"
