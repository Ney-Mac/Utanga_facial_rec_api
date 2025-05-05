from src.models.Turma import  Turma
from src.models.Aluno import Aluno
from src.utils.StatusAluno import StatusAluno


class TurmaAluno:
    def __init__(self, turma: Turma, aluno: Aluno, status: StatusAluno):
        self.turma = turma
        self.aluno = aluno
        self.status = status

    def obterStatus(self):
        return self.status
