

class NotaProva:
    def __init__(self, aluno_id: int, prova_id: int, nota: float):
        self.aluno = aluno_id
        self.prova = prova_id
        self.nota = nota

    def verNota(self):
        return self.nota
