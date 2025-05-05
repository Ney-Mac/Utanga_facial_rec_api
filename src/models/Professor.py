from src.models.Usuario import Usuario
from src.models.Aluno import Aluno
from src.models.Turma import Turma
from src.utils.TipoUsuario import TipoUsuario


class Professor(Usuario):
    def __init__(self, nome: str, numFuncionario: str, foto_hash: str, departamento: str):
        super().__init__(nome=nome, tipo=TipoUsuario.PROFESSOR, codigo_acesso=numFuncionario, foto_hash=foto_hash)
        self.departamento = departamento

    def listarTurmas(self):
        return "Listar turmas"

    def autorizarAcesso(self, aluno: Aluno, turma: Turma, prova: str):
        return "Autorizar Acesso"
