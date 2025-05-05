import TurmaAluno
from datetime import date
from src.utils.StatusPresenca import StatusPresenca


class Presenca:
    def __init__(self, turma_aluno: TurmaAluno, data: date, status: StatusPresenca):
        self.turma_aluno = turma_aluno
        self.data = data
        self.status = status

    def registrarPresenca(self) -> bool:
        print("Registrar presenca")
        return True
