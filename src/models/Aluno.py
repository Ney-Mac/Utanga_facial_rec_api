from src.models.Usuario import Usuario
from src.utils.TipoUsuario import TipoUsuario


class Aluno(Usuario):
    def __init__(self, nome: str, numMatricula: str, foto_hash: str, curso: str):
        super().__init__(nome=nome, tipo=TipoUsuario.ALUNO, codigo_acesso=numMatricula, foto_hash=foto_hash)
        self.curso = curso

    def calcularMedia(self):
        return "Calcular media"

    def verificarDispensa(self):
        return "Verificar Dispensa"
